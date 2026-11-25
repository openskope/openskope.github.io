from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_outline import check_outline


class OutlineTests(unittest.TestCase):
    def test_mixed_headings_have_one_complete_outline(self):
        html = '<aside><div data-skope-outline><nav id="TableOfContents"><ul><li><a href="#guide">User Guide</a><ul><li><a href="#step">A step</a></li></ul></li></ul></nav></div></aside><main><h1>Page</h1><h2 id="guide"><a href="/guide/">User Guide</a></h2><h3 id="step">A step</h3></main>'
        self.assertEqual(check_outline(html), [])
        self.assertIn('On this page must match', check_outline(html.replace('<li><a href="#step">A step</a></li>', ''))[0])
        self.assertIn('missing its outline anchor', check_outline(html.replace(' id="step"', ''))[0])

    def test_short_pages_and_deliberate_opt_out(self):
        self.assertEqual(check_outline('<div data-skope-outline></div><main><h1>Short page</h1></main>'), [])
        self.assertEqual(check_outline('<div data-skope-outline data-outline-disabled></div><main><h2>Hidden outline</h2></main>'), [])
