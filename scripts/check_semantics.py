"""Small rendered-HTML regression guard; browser/axe audits cover the full UI."""
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Semantics(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.anchors = []
        self.errors = []
        self.mains = 0
        self.heading = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'main' or attrs.get('role') == 'main':
            self.mains += 1
        if self.stack and self.stack[-1] in ('ul', 'ol') and tag not in ('li', 'script', 'template'):
            self.errors.append('List has a direct child other than li')
        if tag == 'a':
            if self.anchors:
                self.errors.append('Nested anchors')
            self.anchors.append({'interactive': 'href' in attrs, 'name': attrs.get('aria-label') or attrs.get('title') or attrs.get('aria-labelledby', ''), 'text': ''})
        if tag == 'img':
            if not attrs.get('width', '').isdigit() or not attrs.get('height', '').isdigit():
                self.errors.append('Image needs intrinsic dimensions')
            for anchor in self.anchors:
                anchor['text'] += attrs.get('alt', '')
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            rank = int(tag[1])
            if rank > self.heading + 1:
                self.errors.append('Skipped heading level')
            self.heading = rank
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == 'a' and self.anchors:
            anchor = self.anchors.pop()
            if anchor['interactive'] and not (anchor['name'] or anchor['text'].strip()):
                self.errors.append('Unnamed anchor')
        if tag in self.stack:
            del self.stack[len(self.stack) - 1 - self.stack[::-1].index(tag):]

    def handle_data(self, data):
        for anchor in self.anchors:
            anchor['text'] += data


def check_semantics(html):
    parser = Semantics()
    parser.feed(html)
    if parser.mains != 1:
        parser.errors.append('Expected exactly one main landmark')
    return sorted(set(parser.errors))
