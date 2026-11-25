"""Check rendered page coverage, local links, media and search for root/subpath builds."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit
from check_web_assets import validate, validate_root_citation
from check_semantics import check_semantics
from check_outline import check_outline

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
        self.footers = 0
        self.shared_footers = 0
        self.in_footer = False
        self.footer_text = []
        self.footer_links = []
        self.stylesheets = []
        self.redirect = False
        self.text = []
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag == 'footer':
            self.footers += 1
            self.shared_footers += 'skope-footer' in attrs.get('class', '').split()
            self.in_footer = True
        if tag == 'a' and self.in_footer:
            self.footer_links.append(attrs.get('href'))
        if tag == 'link' and 'stylesheet' in attrs.get('rel', '').split():
            self.stylesheets.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            self.redirect = True
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag=='a' and attrs.get('name'): self.ids.add(attrs['name'])
        for key in ('href','src'):
            if attrs.get(key): self.links.append((tag,key,attrs[key]))
        for candidate in attrs.get('srcset', '').split(','):
            if candidate.strip():
                self.links.append((tag, 'srcset', candidate.split()[0]))

    def handle_endtag(self, tag):
        if tag == 'footer':
            self.in_footer = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_footer:
            self.footer_text.append(data)


def check_footer(parser, footer, prefix):
    """Aliases redirect; every actual page must render the shared footer once."""
    if parser.redirect:
        return []
    errors = []
    if parser.footers != 1 or parser.shared_footers != 1:
        errors.append('Expected exactly one shared footer')
    styles = [href for href in parser.stylesheets
              if re.fullmatch(re.escape(prefix) + r'/css/skope-footer\.min\.[a-f0-9]{64}\.css', href)]
    if len(styles) != 1:
        errors.append('Expected exactly one fingerprinted shared footer stylesheet')
    def normalized(value):
        return ' '.join(value.split())

    actual = normalized(''.join(parser.footer_text))
    for paragraph in footer['acknowledgments']:
        if normalized(''.join(segment['text'] for segment in paragraph)) not in actual:
            errors.append('Missing shared acknowledgment text')
        for segment in paragraph:
            if 'href' in segment and segment['href'] not in parser.footer_links:
                errors.append(f'Missing acknowledgment link: {segment["href"]}')
    if footer['copyright']['holder'] not in actual:
        errors.append('Missing shared copyright holder')
    for name in ('citation', 'terms'):
        if (prefix + footer['content_links'][name] not in parser.footer_links
                or footer['labels'][name] not in actual):
            errors.append(f'Missing shared footer action: {name}')
    return errors


def check(output, base_url):
    try:
        footer = validate(Path('shared/web'))
        validate_root_citation(Path('.'))
    except (ValueError, OSError) as error:
        print(f'Shared web assets: {error}')
        return 1
    report=json.loads(Path('docs/migration/wordpress-import.json').read_text())
    base=urlsplit(base_url); prefix=base.path.rstrip('/')
    errors=[]; pages=list(output.rglob('*.html')); parsed={}
    for path in pages:
        parser=Links(); parser.feed(path.read_text()); parsed[path]=parser
        errors.extend(f'{path}: {error}' for error in check_footer(parser, footer, prefix))
        if not parser.redirect:
            errors.extend(f'{path}: {error}' for error in check_semantics(path.read_text()))
            errors.extend(f'{path}: {error}' for error in check_outline(path.read_text()))
    policy = json.loads(Path('shared/web/application-policy.json').read_text())
    for name, field in [('citation', 'citationGuidance'), ('terms', 'terms')]:
        path = output / footer['content_links'][name].strip('/') / 'index.html'
        if path not in parsed or ' '.join(policy[field].split()) not in ' '.join(''.join(parsed[path].text).split()):
            errors.append(f'Missing shared policy text: {path}')
    citation = output / 'citation/CITATION.cff'
    if not citation.is_file() or citation.read_bytes() != Path('shared/web/CITATION.cff').read_bytes():
        errors.append('Published CITATION.cff differs from the shared source')
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
