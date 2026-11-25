"""Regression checks for the shared bundle's publication contract."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_web_assets import contrast, validate
from check_site import Links, check_footer

SOURCE = Path(__file__).resolve().parents[1] / 'shared/web'


class BundleTests(unittest.TestCase):
    def test_current_bundle_and_footer_contrast(self):
        validate(SOURCE)
        # Reference contrast values verify the luminance calculation itself.
        self.assertAlmostEqual(contrast('#000000', '#ffffff'), 21)
        self.assertAlmostEqual(contrast('#ffffff', '#ffffff'), 1)

    def test_invalid_bundles_are_rejected_before_publication(self):
        cases = [
            ('footer.json', lambda x: x.update(schema_version=2), 'schema_version'),
            ('footer.json', lambda x: x['labels'].pop('terms'), 'label: terms'),
            ('footer.json', lambda x: x['copyright'].update(start_year=True), 'start_year'),
            ('footer.json', lambda x: x.update(acknowledgments=[]), 'acknowledgments'),
            ('footer.json', lambda x: x['acknowledgments'][0][0].update(text=''), 'text'),
            ('footer.json', lambda x: x['acknowledgments'][0][0].update(href='http://example.org'), 'HTTPS'),
            ('footer.json', lambda x: x['content_links'].update(terms='//example.org/'), 'content link'),
            ('tokens.json', lambda x: x['css_variables'].pop('--skope-footer-padding'), 'Missing CSS tokens'),
            ('tokens.json', lambda x: x['css_variables'].pop('--skope-font-family-sans'), 'Missing CSS tokens'),
            ('tokens.json', lambda x: x['css_variables'].update({'--skope-footer-color': 'red; }'}), 'Invalid CSS token'),
            ('tokens.json', lambda x: x['css_variables'].update({'--skope-footer-action-hover-background': '#ffffff'}), 'contrast below'),
            ('application-policy.json', lambda x: x.pop('terms'), 'policy: terms'),
        ]
        for name, mutate, error in cases:
            with self.subTest(name=name, error=error), tempfile.TemporaryDirectory() as tmp:
                bundle = Path(tmp) / 'web'
                shutil.copytree(SOURCE, bundle)
                file = bundle / name
                data = json.loads(file.read_text())
                mutate(data)
                file.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, error):
                    validate(bundle)

    def test_missing_citation_metadata_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / 'web'
            shutil.copytree(SOURCE, bundle)
            citation = bundle / 'CITATION.cff'
            citation.write_text(citation.read_text().replace('doi:', 'missing-doi:'))
            with self.assertRaisesRegex(ValueError, 'citation metadata: doi'):
                validate(bundle)

    def test_empty_citation_field_cannot_borrow_the_next_line(self):
        for value in ('', '""'):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                bundle = Path(tmp) / 'web'
                shutil.copytree(SOURCE, bundle)
                citation = bundle / 'CITATION.cff'
                lines = citation.read_text().splitlines()
                citation.write_text('\n'.join('title: ' + value if line.startswith('title:') else line for line in lines))
                with self.assertRaisesRegex(ValueError, 'citation metadata: title'):
                    validate(bundle)


class RenderedFooterTests(unittest.TestCase):
    footer = {
        'copyright': {'holder': 'SKOPE'},
        'acknowledgments': [[{'text': 'Supported by '}, {'text': 'Research', 'href': 'https://example.org/'}]],
        'labels': {'citation': 'Cite SKOPE', 'terms': 'Terms of Use'},
        'content_links': {'citation': '/cite-skope/', 'terms': '/terms-of-use/'},
    }

    def markup(self, prefix=''):
        return (f'<link rel="stylesheet" href="{prefix}/css/skope-footer.min.{"a" * 64}.css">'
                '<footer class="td-footer skope-footer"><p>Supported by '
                '<a href="https://example.org/">Research</a></p><span>SKOPE</span>'
                f'<a href="{prefix}/cite-skope/">Cite SKOPE</a>'
                f'<a href="{prefix}/terms-of-use/">Terms of Use</a></footer>')

    def check(self, markup, prefix=''):
        parser = Links()
        parser.feed(markup)
        return check_footer(parser, self.footer, prefix)

    def test_root_and_subpath_pages(self):
        for prefix in ('', '/preview'):
            with self.subTest(prefix=prefix):
                self.assertEqual(self.check(self.markup(prefix), prefix), [])

    def test_missing_or_duplicate_footer_and_stylesheet(self):
        self.assertIn('Expected exactly one shared footer', self.check(''))
        self.assertIn('Expected exactly one shared footer', self.check(self.markup() * 2))
        self.assertIn('Expected exactly one fingerprinted shared footer stylesheet',
                      self.check(self.markup().replace('rel="stylesheet"', 'rel="preload"')))

    def test_missing_content_and_links(self):
        self.assertIn('Missing shared acknowledgment text', self.check(self.markup().replace('Supported by', '')))
        self.assertIn('Missing shared footer action: terms', self.check(self.markup().replace('/terms-of-use/', '/wrong/')))
        self.assertIn('Missing shared footer action: terms', self.check(self.markup(), '/preview'))

    def test_alias_redirect_does_not_need_a_footer(self):
        self.assertEqual(self.check('<meta http-equiv="refresh" content="0; url=/guide/">'), [])


if __name__ == '__main__':
    unittest.main()
