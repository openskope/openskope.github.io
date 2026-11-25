"""Fetch pinned WOFF2 fonts and licenses; verify all bytes before replacing files."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import urlsplit
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/'data/fonts.json'

def main():
    config=json.loads(LOCK.read_text())
    update=os.environ.get('FONT_UPDATE_LOCK','')=='1'
    pending=[]
    with tempfile.TemporaryDirectory() as tmp:
        for index,entry in enumerate(config['faces']+config['licenses']):
            url=entry['source_url'];parts=urlsplit(url)
            if parts.scheme!='https' or parts.hostname not in {'fonts.gstatic.com','raw.githubusercontent.com'}:
                raise ValueError('Font source must use the approved HTTPS upstreams')
            relative=Path('assets')/entry['asset'] if 'asset' in entry else Path(entry['path'])
            dest=(ROOT/relative).resolve()
            if not dest.is_relative_to(ROOT/'assets/fonts') and not dest.is_relative_to(ROOT/'static/fonts'):
                raise ValueError('Font destination escapes fonts directories')
            with urlopen(url,timeout=30) as response:data=response.read()
            if 'asset' in entry and not data.startswith(b'wOF2'):raise ValueError(f'Not WOFF2: {url}')
            digest=hashlib.sha256(data).hexdigest()
            if not update and digest!=entry.get('sha256'):
                raise ValueError(f'Checksum mismatch for {relative}; review upstream before updating the lock')
            entry['sha256']=digest
            staging=Path(tmp)/str(index);staging.write_bytes(data);pending.append((staging,dest))
        for staging,dest in pending:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(staging.read_bytes())
    if update:LOCK.write_text(json.dumps(config,indent=2)+'\n')
    print(f'Installed {len(config["faces"])} WOFF2 faces and {len(config["licenses"])} licenses; checksums '+('recorded' if update else 'verified'))

if __name__=='__main__':main()
