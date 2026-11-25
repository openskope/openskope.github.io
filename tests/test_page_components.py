"""Exercise native Hugo outlines, Markdown headings and shared actions."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ComponentMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.heading_ids = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'a' and 'skope-action' in attrs.get('class', '').split():
            self.buttons.append(attrs)
        if tag in ('h2', 'h3', 'h4'):
            self.heading_ids.append(attrs.get('id'))


class PageComponentTests(unittest.TestCase):
    def test_outline_preserves_ids_and_actions_use_the_site_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'content/users-guide').mkdir(parents=True)
            (root / 'layouts/partials/skope').mkdir(parents=True)
            for name in ('action', 'actions'):
                shutil.copyfile(ROOT / f'layouts/partials/skope/{name}.html', root / f'layouts/partials/skope/{name}.html')
            (root / 'hugo.yaml').write_text('''baseURL: https://example.org/preview/
markup:
  goldmark:
    renderer:
      unsafe: true
menu:
  main:
    - name: Launch fixture
      identifier: launch-skope
      url: https://app.example.org/
''')
            (root / 'content/users-guide/index.md').write_text('---\ntitle: Fixture Guide\n---\nGuide text.\n')
            (root / 'content/_index.md').write_text('''---
title: Mixed headings
---
## Markdown title

<section class="fixture" aria-labelledby="kept">

## [HTML guide](/users-guide/) {#kept}

### Shared &amp; safe

## Repeat

## Repeat

</section>
''')
            (root / 'layouts/home.html').write_text('''{{ .Content }}
{{ .TableOfContents }}
{{ partial "skope/actions.html" (dict "page" .) }}''')
            result = subprocess.run(['hugo', '--source', str(root), '--destination', str(root / 'public'), '--quiet'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = (root / 'public/index.html').read_text()
            markup = ComponentMarkup()
            markup.feed(output)
            self.assertEqual(markup.heading_ids, ['markdown-title', 'kept', 'shared--safe', 'repeat', 'repeat-1'])
            self.assertIn('<section class="fixture" aria-labelledby="kept">', output)
            self.assertIn('<a href="#kept">HTML guide</a>', output)
            self.assertIn('<a href="#shared--safe">Shared &amp; safe</a>', output)
            self.assertEqual(len(markup.buttons), 2)
            launch, guide = markup.buttons
            self.assertEqual(launch['href'], 'https://app.example.org/')
            self.assertEqual(launch['aria-label'], 'Launch fixture (opens in a new tab)')
            self.assertEqual(launch['target'], '_blank')
            self.assertIn('noopener', launch['rel'])
            self.assertEqual(guide['href'], '/preview/users-guide/')
            self.assertIn('Fixture Guide', output)

    def test_figures_and_inline_icons_share_responsive_images(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'content').mkdir()
            (root / 'layouts/shortcodes').mkdir(parents=True)
            (root / 'layouts/partials/skope').mkdir(parents=True)
            (root / 'assets/legacy-images').mkdir(parents=True)
            (root / 'assets/screenshots').mkdir(parents=True)
            for name in ('skope-figure', 'legacy-image'):
                shutil.copyfile(ROOT / f'layouts/shortcodes/{name}.html', root / f'layouts/shortcodes/{name}.html')
            shutil.copyfile(ROOT / 'layouts/partials/skope/image.html', root / 'layouts/partials/skope/image.html')
            shutil.copyfile(ROOT / 'static/wp-content/uploads/2018/05/cropped-AltHeadeID-1-32x32.png', root / 'assets/legacy-images/fixture.png')
            shutil.copyfile(root / 'assets/legacy-images/fixture.png', root / 'assets/screenshots/fixture.png')
            (root / 'hugo.yaml').write_text('baseURL: https://example.org/preview/\n')
            (root / 'layouts/home.html').write_text('{{ .Content }}')
            (root / 'content/_index.md').write_text('''---
title: Figure fixture
---
{{< skope-figure src="screenshots/fixture.png" alt="Chart" width="320" caption="**Chart caption**" align="right" class="fixture-figure" eager=true link="wp-content/uploads/original.png" >}}

An inline icon {{< legacy-image src="wp-content/uploads/fixture.png" alt="" width="22" >}} stays inline.
''')
            result = subprocess.run(['hugo', '--source', str(root), '--quiet'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = (root / 'public/index.html').read_text()
            self.assertEqual(output.count('<figure '), 1)
            self.assertEqual(output.count('<img '), 2)
            self.assertIn('class="skope-figure alignright fixture-figure"', output)
            self.assertIn('<figcaption><strong>Chart caption</strong></figcaption>', output)
            self.assertIn('srcset="/preview/screenshots/', output)
            self.assertIn('loading="eager"', output)
            self.assertIn('<a href="/preview/wp-content/uploads/original.png">', output)
            self.assertIn('alt="Chart"', output)
            self.assertIn('alt=""', output)
            self.assertIn('src="/preview/wp-content/uploads/fixture.png"', output)
            self.assertIn('width="22" height="22"', output)
            self.assertIn('loading="lazy"', output)
            self.assertRegex(output, r'An inline icon <img[^>]+>\s+stays inline')
