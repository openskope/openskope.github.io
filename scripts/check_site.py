"""Check rendered page coverage, local links, media and search for root/subpath builds."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag=='a' and attrs.get('name'): self.ids.add(attrs['name'])
        for key in ('href','src'):
            if attrs.get(key): self.links.append((tag,key,attrs[key]))


def check(output, base_url):
    report=json.loads(Path('docs/migration/wordpress-import.json').read_text())
    base=urlsplit(base_url); prefix=base.path.rstrip('/')
    errors=[]; pages=list(output.rglob('*.html')); parsed={}
    for path in pages:
        parser=Links(); parser.feed(path.read_text()); parsed[path]=parser
    for entry in report['published_pages']:
        path=output/entry['path']/'index.html'
        if not path.is_file(): errors.append(f'Missing imported page: {path}')
    review=json.loads(Path('docs/migration/review.json').read_text())
    retired=review['retired_media']
    for old,new in review.get('route_changes',{}).items():
        canonical=output/new.strip('/')/'index.html'
        legacy=output/old.strip('/')/'index.html'
        if not canonical.is_file(): errors.append(f'Missing canonical route: {new}')
        if not legacy.is_file(): errors.append(f'Missing legacy alias: {old}')
        elif base_url.rstrip('/')+new not in legacy.read_text():
            errors.append(f'Legacy alias {old} does not redirect to {new}')

    media=json.loads(Path('docs/migration/media.json').read_text())
    for entry in media:
        if entry['path'] in retired: continue
        path=output/entry['path'].lstrip('/')
        if 'errors' in entry or not path.is_file(): errors.append(f'Missing media: {path}')
        elif hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
            errors.append(f'Media checksum mismatch: {path}')
    fonts=json.loads(Path('data/fonts.json').read_text())
    for face in fonts['faces']:
        asset=Path(face['asset'])
        source=Path('assets')/asset
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=face['sha256']:
            errors.append(f'Font source checksum mismatch: {source}')
        expected=output/asset.parent/(asset.stem+'.'+face['sha256']+asset.suffix)
        if not expected.is_file() or hashlib.sha256(expected.read_bytes()).hexdigest()!=face['sha256']:
            errors.append(f'Missing or incorrect fingerprinted font: {expected}')
    for license in fonts['licenses']:
        expected=output/Path(license['path']).relative_to('static')
        if not expected.is_file() or hashlib.sha256(expected.read_bytes()).hexdigest()!=license['sha256']:
            errors.append(f'Missing or incorrect font license: {expected}')
    missing_fragments=set()
    for path,parser in parsed.items():
        route='/' + str(path.relative_to(output)).removesuffix('index.html')
        current=base_url.rstrip('/') + route
        for tag,key,link in parser.links:
            target=urlsplit(urljoin(current,link))
            if target.scheme not in ('http','https') or target.netloc!=base.netloc: continue
            local=unquote(target.path)
            if prefix and not (local==prefix or local.startswith(prefix+'/')):
                errors.append(f'{path}: link escapes deployment prefix: {link}'); continue
            relative=local[len(prefix):].lstrip('/')
            candidate=output/relative
            if candidate.is_dir(): candidate=candidate/'index.html'
            if not candidate.exists():
                # Hugo emits theme-owned cosmetic favicon links only if configured.
                errors.append(f'{path}: missing {link}'); continue
            if target.fragment and candidate in parsed and unquote(target.fragment) not in parsed[candidate].ids:
                missing_fragments.add(f'{path}: missing anchor {link}')
    # Imported HTML can contain historical anchors. Report those separately for review.
    search=list(output.glob('**/*offline-search-index*.json'))
    if not search: errors.append('Missing Docsy offline search index')
    if (output/'CNAME').read_text().strip()!='www.openskope.org': errors.append('Wrong custom domain')
    for item in sorted(set(errors)): print(item)
    for item in sorted(missing_fragments): print('ANCHOR REVIEW:',item)
    print(f'{len(pages)} HTML pages; {len(report["published_pages"])} imported routes; {sum(e['path'] not in retired for e in media)} archived media files; {len(retired)} documented retired references; {len(missing_fragments)} anchor warnings; {len(set(errors))} errors')
    return len(set(errors))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    parser.add_argument('--base-url',default='https://www.openskope.org/')
    args=parser.parse_args()
    raise SystemExit(bool(check(args.output,args.base_url)))
