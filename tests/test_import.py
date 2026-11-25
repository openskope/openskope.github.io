import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('importer', Path(__file__).resolve().parents[1]/'scripts/import_wordpress.py')
importer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)

class ImportTests(unittest.TestCase):
    def test_published_only_and_control_character(self):
        data=b'''<rss xmlns:wp="http://wordpress.org/export/1.2/"><channel><item><title>Public\x0bpage</title><link>https://www.openskope.org/public</link><wp:post_type>page</wp:post_type><wp:status>publish</wp:status><wp:post_id>1</wp:post_id></item><item><wp:post_type>page</wp:post_type><wp:status>draft</wp:status><title>Private draft</title></item></channel></rss>'''
        pages, skipped, count=importer.parse_export(data)
        self.assertEqual([p['title'] for p in pages], ['Public page'])
        self.assertEqual(skipped, {'page:draft':1})
        self.assertEqual(count,1)
    def test_password_protected_published_page_excluded(self):
        data = b'''<rss xmlns:wp="http://wordpress.org/export/1.2/"><channel><item><wp:post_type>page</wp:post_type><wp:status>publish</wp:status><wp:post_password>private</wp:post_password></item></channel></rss>'''
        pages, skipped, _ = importer.parse_export(data)
        self.assertEqual(pages, [])
        self.assertEqual(skipped, {'page:password-protected': 1})

    def test_internal_links_and_local_media_use_hugo_helpers(self):
        media={}
        body=importer.rewrite('<a href="http://www.openskope.org/guide#help">Guide</a><img src="http://www.envirecon.org/wp-content/uploads/a.png" srcset="other.png 2x">', {'guide'}, {}, media, set())
        self.assertIn('{{< relref "/guide" >}}#help',body)
        self.assertIn('{{< siteurl "wp-content/uploads/a.png" >}}',body)
        self.assertNotIn('srcset',body)
        self.assertEqual(list(media),['/wp-content/uploads/a.png'])
    def test_does_not_overwrite_reviewed_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp); (out/'reviewed.md').write_text('keep')
            with self.assertRaisesRegex(ValueError,'not empty'):
                importer.import_export(Path('unused.xml'),out)
            self.assertEqual((out/'reviewed.md').read_text(),'keep')
    def test_active_content_rejected(self):
        for body in ['<script>alert(1)</script>', '<img onerror="x">', '<a href="javascript:x">x</a>']:
            with self.subTest(body=body), self.assertRaises(ValueError):
                importer.rewrite(body,set(),{},{},set())
    def test_unknown_links_reported_without_changing_external_references(self):
        unknown=set()
        body=importer.rewrite('<a href="https://www.openskope.org/missing">x</a><a href="https://example.org/">y</a>',set(),{},{},unknown)
        self.assertEqual(unknown,{'https://www.openskope.org/missing'})
        self.assertIn('https://example.org/',body)
    def test_media_traversal_rejected(self):
        with self.assertRaises(ValueError):
            importer.rewrite('<img src="/wp-content/uploads/../secret">',set(),{},{},set())

if __name__=='__main__': unittest.main()
