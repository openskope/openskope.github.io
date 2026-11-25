"""Check that generated section navigation matches the visible page headings."""
from html.parser import HTMLParser
from urllib.parse import unquote
from check_semantics import VOID


class Outline(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.main = None
        self.toc = None
        self.heading = None
        self.link = None
        self.headings = []
        self.links = []
        self.enabled = False
        self.disabled = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag not in VOID:
            self.depth += 1
        if 'data-skope-outline' in attrs:
            self.enabled = True
            self.disabled = 'data-outline-disabled' in attrs
        if tag == 'main':
            self.main = self.depth
        if self.main is not None and tag in ('h2', 'h3', 'h4'):
            self.heading = {'id': attrs.get('id'), 'text': '', 'tag': tag}
        if tag == 'nav' and attrs.get('id') == 'TableOfContents':
            self.toc = self.depth
        if self.toc is not None and tag == 'a':
            self.link = {'id': unquote(attrs.get('href', '').removeprefix('#')), 'text': ''}

    def handle_endtag(self, tag):
        if self.heading is not None and tag == self.heading['tag']:
            self.headings.append(self.heading)
            self.heading = None
        if self.link is not None and tag == 'a':
            self.links.append(self.link)
            self.link = None
        if self.depth == self.main and tag == 'main':
            self.main = None
        if self.depth == self.toc and tag == 'nav':
            self.toc = None
        if tag not in VOID:
            self.depth -= 1

    def handle_data(self, text):
        if self.heading is not None:
            self.heading['text'] += text
        if self.link is not None:
            self.link['text'] += text


def check_outline(html):
    parser = Outline()
    parser.feed(html)
    if not parser.enabled or parser.disabled:
        return []
    headings = [entry for entry in parser.headings if entry['text'].strip()]
    if any(not entry['id'] for entry in headings):
        return ['Section heading is missing its outline anchor']
    ids = [entry['id'] for entry in headings]
    if len(set(ids)) != len(ids):
        return ['Duplicate section heading anchors']
    normalized = lambda entries: [(entry['id'], ' '.join(entry['text'].split())) for entry in entries]
    if normalized(headings) != normalized(parser.links):
        return ['On this page must match the section headings in reading order']
    return []
