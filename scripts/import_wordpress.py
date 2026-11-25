"""Import published WXR pages, preserving prose and HTML without WordPress runtime."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

NS = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/'}
LEGACY_HOSTS = {'www.openskope.org', 'openskope.org', 'www.envirecon.org', 'envirecon.org'}
CONTROL = re.compile(rb'[\x00-\x08\x0b\x0c\x0e-\x1f]')
ATTR = re.compile(r'\b(href|src|srcset)\s*=\s*([\"\x27])(.*?)\2', re.I | re.S)

def parse_export(data):
    cleaned, count = CONTROL.subn(b' ', data)
    channel = ET.fromstring(cleaned).find('channel')
    if channel is None:
        raise ValueError('Missing WordPress channel')
    pages, skipped = [], {}
    for item in channel.findall('item'):
        kind = item.findtext('wp:post_type', namespaces=NS)
        status = item.findtext('wp:status', namespaces=NS)
        protected = bool(item.findtext('wp:post_password', '', namespaces=NS))
        if kind not in ('page', 'post') or status != 'publish' or protected:
            key = f'{kind}:password-protected' if protected else f'{kind}:{status}'
            skipped[key] = skipped.get(key, 0) + 1
            continue
        url = item.findtext('link', '')
        path = unquote(urlsplit(url).path).strip('/')
        if '..' in path.split('/') or urlsplit(url).hostname not in LEGACY_HOSTS:
            raise ValueError(f'Unsafe page URL: {url}')
        if not path and any(not p['path'] for p in pages):
            raise ValueError('Multiple home pages')
        pages.append({'id': item.findtext('wp:post_id', namespaces=NS),
                      'title': html.unescape(item.findtext('title', '')),
                      'url': url, 'path': path,
                      'modified': item.findtext('wp:post_modified_gmt', namespaces=NS),
                      'body': item.findtext('content:encoded', '', namespaces=NS)})
    if len({p['path'] for p in pages}) != len(pages):
        raise ValueError('Duplicate page paths')
    return pages, skipped, count

def rewrite(body, page_paths, page_ids, media, unresolved):
    # Gutenberg comments contain editor configuration, not reader-facing content.
    body = re.sub(r'<!--[\s\S]*?-->', '', body)
    if re.search(r'<\s*(script|iframe|form|object)\b|\bon\w+\s*=', body, re.I):
        raise ValueError('Active HTML needs explicit review before import')
    def url(value):
        value = html.unescape(value)
        parts = urlsplit(value)
        if parts.scheme.lower() in ('javascript', 'data', 'vbscript'):
            raise ValueError('Active URL needs explicit review')
        if parts.hostname not in LEGACY_HOSTS and not (value.startswith('/') and not value.startswith('//')):
            return html.escape(value, quote=True)
        path = unquote(parts.path)
        if '..' in path.split('/'):
            raise ValueError('Unsafe local URL')
        suffix = ('#' + parts.fragment) if parts.fragment else ''
        if path.startswith('/wp-content/uploads/'):
            media.setdefault(path, set()).add(value)
            return '{{< siteurl ' + json.dumps(path.lstrip('/')) + ' >}}' + suffix
        target = path.strip('/')
        if parts.query.startswith('page_id='):
            target = page_ids.get(parts.query.split('=', 1)[1], target)
        if target in page_paths:
            ref = '/' + target if target else '/'
            return '{{< relref ' + json.dumps(ref) + ' >}}' + suffix
        unresolved.add(value)
        return html.escape(value, quote=True)
    def attr(match):
        name, quote, value = match.groups()
        if name.lower() == 'srcset':
            # Fetch the referenced src image; drop WordPress-generated alternatives.
            return ''
        result = url(value)
        # Shortcodes contain quoted arguments, so use single-quoted HTML attributes.
        return name + "='" + result.replace("'", '&#x27;') + "'"
    return ATTR.sub(attr, body).strip() + '\n'

def import_export(source, output):
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output is not empty; import into a new review directory')
    data = source.read_bytes()
    pages, skipped, controls = parse_export(data)
    paths = {p['path'] for p in pages}
    ids = {p['id']: p['path'] for p in pages}
    media, unresolved, records = {}, set(), []
    rendered = []
    for page in pages:
        body = rewrite(page['body'], paths, ids, media, unresolved)
        front = {'title': page['title'], 'wordpress_id': int(page['id'])}
        if page['path']:
            front['type'] = 'docs'
        if page['modified'] and not page['modified'].startswith('0000'):
            front['lastmod'] = page['modified'].replace(' ', 'T') + 'Z'
        dest = 'content/' + (page['path'] + '/index.md' if page['path'] else '_index.md')
        rendered.append((dest, json.dumps(front, indent=2, ensure_ascii=False) + '\n\n' + body))
        records.append({k:page[k] for k in ('id','title','url','path')})
    for name, text in rendered:
        dest = output/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
    report = {'source_file': source.name, 'source_sha256': hashlib.sha256(data).hexdigest(),
              'xml_control_characters_replaced_in_memory': controls, 'published_pages': records,
              'excluded_item_counts': skipped, 'unresolved_legacy_links': sorted(unresolved),
              'media': [{'path':p, 'source_urls':sorted(urls)} for p,urls in sorted(media.items())]}
    dest = output/'docs/migration/wordpress-import.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    print(f'Imported {len(pages)} pages; {len(media)} media references; {len(unresolved)} unresolved legacy links')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    import_export(args.source, args.output)
