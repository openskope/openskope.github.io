import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_semantics import check_semantics


class SemanticsTests(unittest.TestCase):
    def test_named_links_images_and_headings(self):
        self.assertEqual(check_semantics('<main><h1>Title</h1><a id="chapter"></a><h2>Section</h2><a href="/chart"><img alt="Chart" width="320" height="200"></a><a href="/code" aria-label="Source"></a><ul><li>One<ul><li>Child</li></ul></li></ul></main>'), [])

    def test_rendering_regressions(self):
        cases = [
            ('<main><a href="/x"><a href="/x">URL</a></a></main>', 'Nested anchors'),
            ('<main><a href="/x"></a></main>', 'Unnamed anchor'),
            ('<main><h1>Title</h1><h3>Section</h3></main>', 'Skipped heading level'),
            ('<main><ul><ul><li>Item</li></ul></ul></main>', 'List has a direct child other than li'),
            ('<main><main>Text</main></main>', 'Expected exactly one main landmark'),
            ('<main><img alt="Chart"></main>', 'Image needs intrinsic dimensions'),
        ]
        for markup, error in cases:
            with self.subTest(error=error):
                self.assertIn(error, check_semantics(markup))
