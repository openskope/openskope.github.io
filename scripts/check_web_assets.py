"""Validate the website-owned v1 shared bundle before rendering or publishing."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

TOKEN = re.compile(r'var\(\s*(--skope-[a-z-]+)')


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def contrast(first, second):
    def luminance(value):
        if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise ValueError('Footer contrast colors must use six-digit hex values')
        channels = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        return sum((c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4) * w
                   for c, w in zip(channels, (.2126, .7152, .0722)))
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + .05) / (darker + .05)


def validate(directory):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def read_json(name):
        value = json.loads((directory / name).read_text())
        require(isinstance(value, dict), f'{name}: expected an object')
        return value

    footer = read_json('footer.json')
    tokens = read_json('tokens.json')
    policy = read_json('application-policy.json')
    for name, data in [('footer.json', footer), ('tokens.json', tokens)]:
        require(type(data.get('schema_version')) is int and data['schema_version'] == 1,
                f'{name}: unsupported schema_version; expected 1')
    copyright = footer.get('copyright')
    require(isinstance(copyright, dict), 'Missing footer copyright')
    require(type(copyright.get('start_year')) is int and 1 <= copyright['start_year'] <= 9999,
            'Invalid copyright start_year')
    require(nonempty(copyright.get('holder')), 'Missing copyright holder')
    paragraphs = footer.get('acknowledgments')
    require(isinstance(paragraphs, list) and paragraphs, 'Missing acknowledgments')
    for paragraph in paragraphs:
        require(isinstance(paragraph, list) and paragraph, 'Empty acknowledgment paragraph')
        for segment in paragraph:
            require(isinstance(segment, dict) and nonempty(segment.get('text')),
                    'Missing acknowledgment text')
            if 'href' in segment:
                href = segment['href']
                require(nonempty(href), 'Invalid acknowledgment link')
                url = urlsplit(href)
                require(url.scheme == 'https' and url.hostname and not url.username
                        and not re.search(r'\s', href), 'Acknowledgment links must use HTTPS')
    labels = footer.get('labels', {})
    require(isinstance(labels, dict), 'Invalid footer labels')
    for label in ('citation', 'terms', 'build', 'source'):
        require(nonempty(labels.get(label)), f'Missing footer label: {label}')
    links = footer.get('content_links', {})
    require(isinstance(links, dict), 'Invalid footer content_links')
    for name in ('citation', 'terms'):
        route = links.get(name)
        require(isinstance(route, str) and re.fullmatch(r'/(?:[a-z0-9-]+/)+', route),
                f'Invalid local content link: {name}')

    variables = tokens.get('css_variables')
    require(isinstance(variables, dict) and variables, 'Missing CSS tokens')
    for name, value in variables.items():
        require(re.fullmatch(r'--skope-[a-z-]+', name) and nonempty(value)
                and not re.search(r'[;{}<>]', value), f'Invalid CSS token: {name}')
    css = (directory / 'footer.css').read_text()
    require('.skope-footer' in css, 'Missing footer CSS')
    referenced = set(TOKEN.findall(css + '\n' + '\n'.join(variables.values())))
    missing = referenced - variables.keys()
    require(not missing, f'Missing CSS tokens: {", ".join(sorted(missing))}')
    for background in ('--skope-footer-background', '--skope-footer-action-hover-background'):
        require(background in variables and '--skope-footer-color' in variables,
                f'Missing footer contrast token: {background}')
        ratio = contrast(variables['--skope-footer-color'], variables[background])
        require(ratio >= 4.5, f'Footer contrast below 4.5:1 on {background}: {ratio:.2f}:1')
    for key in ('terms', 'citationGuidance'):
        require(nonempty(policy.get(key)), f'Missing application policy: {key}')
    citation = (directory / 'CITATION.cff').read_text()
    # Hugo parses the full YAML when rendering the citation shortcode.
    for field in ('cff-version', 'title', 'doi', 'url', 'version', 'date-released'):
        match = re.search(rf'^{field}:[ \t]*([^\n]+)$', citation, re.MULTILINE)
        require(match and match[1].strip() not in ('', '""', "''", 'null', '~'),
                f'Missing citation metadata: {field}')
    require(re.search(r'^authors:[ \t]*\n[ \t]*-[ \t]+\S', citation, re.MULTILINE),
            'Missing citation metadata: authors')
    return footer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path, default=Path('shared/web'))
    args = parser.parse_args()
    try:
        validate(args.directory)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Shared web assets: {error}\n')
    print('Shared web assets: schema, links, tokens, contrast and citation fields verified')
