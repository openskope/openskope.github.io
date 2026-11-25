"""Fetch published-page media explicitly; routine builds never fetch WordPress."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

def fetch(record):
    relative = record['path'].lstrip('/')
    if not relative.startswith('wp-content/uploads/') or '..' in relative.split('/'):
        raise ValueError('Unsafe media path')
    dest = ROOT/'static'/relative
    errors = []
    urls = ['https://www.openskope.org/' + quote(relative)]
    urls += [u.replace('http:', 'https:', 1) for u in record['source_urls']]
    for url in dict.fromkeys(urls):
        if urlsplit(url).hostname not in {'www.openskope.org','openskope.org','www.envirecon.org','envirecon.org'}:
            raise ValueError('Unapproved media host')
        try:
            with urlopen(Request(url, headers={'User-Agent':'OpenSKOPE-site-migration/1.0'}), timeout=30) as response:
                kind = response.headers.get_content_type()
                data = response.read()
            if not (kind.startswith('image/') or kind in ('application/pdf','application/octet-stream')):
                raise ValueError(f'Unexpected media content type: {kind}')
            if not data or data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
                raise ValueError('Empty or HTML response')
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
            return {'path':record['path'], 'fetched_from':url, 'sha256':hashlib.sha256(data).hexdigest(), 'bytes':len(data), 'content_type':kind}
        except (URLError, TimeoutError, ValueError) as exc:
            errors.append(str(exc))
    return {'path':record['path'], 'errors':errors}

if __name__ == '__main__':
    records = json.loads((ROOT/'docs/migration/wordpress-import.json').read_text())['media']
    branding=ROOT/'docs/migration/branding.json'
    if branding.exists(): records += json.loads(branding.read_text())
    retired=json.loads((ROOT/'docs/migration/review.json').read_text())['retired_media']
    records=[r for r in records if r['path'] not in retired]
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch, records))
    (ROOT/'docs/migration/media.json').write_text(json.dumps(results, indent=2)+'\n')
    failures = [r for r in results if 'errors' in r]
    print(f'{len(results)-len(failures)}/{len(results)} media files fetched')
    for failure in failures: print(failure)
    raise SystemExit(bool(failures))
