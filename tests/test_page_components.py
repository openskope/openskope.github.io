"""Exercise native Hugo outlines, Markdown headings and shared actions."""
from html.parser import HTMLParser
import hashlib
import json
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

    def test_released_guide_includes_one_frozen_snapshot_with_native_anchors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ('content/users-guide', 'content/guide-versions/v2023.10', 'content/guide-versions/next', 'layouts/shortcodes', 'layouts/partials/skope', 'data'):
                (root / directory).mkdir(parents=True)
            for name in ('released-guide', 'guide-version', 'guide-version-menu'):
                shutil.copyfile(ROOT / f'layouts/shortcodes/{name}.html', root / f'layouts/shortcodes/{name}.html')
            shutil.copyfile(ROOT / 'layouts/partials/skope/guide-version.html', root / 'layouts/partials/skope/guide-version.html')
            shutil.copyfile(ROOT / 'layouts/partials/skope/guide-version-menu.html', root / 'layouts/partials/skope/guide-version-menu.html')
            # Stub only the upstream renderer: the real Docsy dropdown is browser-tested.
            (root / 'layouts/partials/navbar-version-selector.html').write_text('{{ range .Site.Params.versions }}<a href="{{ .url }}">{{ .name | default .version }}</a>{{ end }}')
            shutil.copyfile(ROOT / 'content/guide-versions/_index.md', root / 'content/guide-versions/_index.md')
            (root / 'hugo.yaml').write_text('baseURL: https://example.org/preview/\n')
            (root / 'layouts/single.html').write_text('{{ .Content }}{{ .TableOfContents }}')
            (root / 'content/users-guide/index.md').write_text('---\ntitle: User Guide\n---\n{{% released-guide %}}\n')
            body = '{{< guide-version >}}\n\n## Select Area {#select-area}\n\nFrozen instructions.\n'
            release = root / 'content/guide-versions/v2023.10/index.md'
            release.write_text('---\ntitle: Released guide\nurl: /users-guide/v2023.10/\nguide_version: v2023.10\n---\n' + body)
            (root / 'content/guide-versions/next/index.md').write_text('---\ntitle: Preview\nurl: /users-guide/next/\nguide_version: next\n---\n{{< guide-version >}}\n\n## Draft steps\n')
            catalog = {'latest_released': 'v2023.10', 'releases': [{'version': 'v2023.10', 'app_revision': 'b5f65844b6ac0c5cc38ddb7a5a4362802688f33f', 'guide_page': '/guide-versions/v2023.10', 'content_sha256': hashlib.sha256(body.strip().encode()).hexdigest()}], 'preview': {'guide_page': '/guide-versions/next', 'base_release': 'v2026.11.1', 'app_build': 'v2026.11.1-6-gbd11a16'}}
            params = {'guide_latest_released': catalog['latest_released'], 'versions': [{'name': 'Latest released guide', 'kind': 'latest', 'guide_page': '/users-guide'}] + catalog['releases'] + [{'kind': 'next', **catalog['preview']}]}
            (root / 'hugo.json').write_text(json.dumps({'baseURL': 'https://example.org/preview/', 'params': params}))
            (root / 'hugo.yaml').unlink()
            command = ['hugo', '--source', str(root), '--quiet']
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for path in ('users-guide/index.html', 'users-guide/v2023.10/index.html'):
                output = (root / 'public' / path).read_text()
                self.assertEqual(output.count('Frozen instructions.'), 1)
                self.assertEqual(output.count('aria-label="Guide version"'), 1)
                selector = output.index('class="skope-guide-version-selector"')
                self.assertLess(output.index('aria-label="Guide version"'), selector)
                self.assertLess(selector, output.index('</aside>'))
                for destination in ('/preview/users-guide/', '/preview/users-guide/v2023.10/', '/preview/users-guide/next/'):
                    self.assertIn('href="' + destination + '"', output)
                self.assertIn('<h2 id="select-area">Select Area</h2>', output)
                self.assertIn('href="#select-area"', output)
            preview = (root / 'public/users-guide/next/index.html').read_text()
            self.assertIn('Staging preview', preview)
            self.assertIn('v2026.11.1-6-gbd11a16', preview)
            release.write_text(release.read_text() + '\nUnreviewed change.\n')
            result = subprocess.run(command[:-1], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Frozen guide content changed', result.stdout + result.stderr)
            release.write_text(release.read_text().replace('\nUnreviewed change.\n', ''))
            config = root / 'hugo.json'
            settings = json.loads(config.read_text())
            settings['params']['guide_latest_released'] = 'next'
            config.write_text(json.dumps(settings))
            result = subprocess.run(command[:-1], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Latest published user guide must use a CalVer release', result.stdout + result.stderr)
            settings['params']['guide_latest_released'] = 'v2023.10'
            settings['params']['versions'][1]['guide_page'] = '/guide-versions/next'
            config.write_text(json.dumps(settings))
            result = subprocess.run(command[:-1], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Released guide page must match', result.stdout + result.stderr)
