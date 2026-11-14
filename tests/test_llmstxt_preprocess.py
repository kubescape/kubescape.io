"""Exercise the mkdocs-llmstxt preprocess hook used for the Markdown copies."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

from bs4 import BeautifulSoup

SPEC = spec_from_file_location('llmstxt_preprocess', Path(__file__).resolve().parents[1] / 'scripts/llmstxt_preprocess.py')
llmstxt_preprocess = module_from_spec(SPEC)
SPEC.loader.exec_module(llmstxt_preprocess)


class PreprocessTest(unittest.TestCase):
    def preprocess(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        llmstxt_preprocess.preprocess(soup, 'site/guide/index.md')
        return soup

    def test_directive_comes_first_and_links_to_llms_txt(self):
        soup = self.preprocess('<h1>Guide</h1><p>Body</p>')
        first = soup.contents[0]
        self.assertEqual(first.name, 'p')
        self.assertTrue(first.get_text().startswith(llmstxt_preprocess.DIRECTIVE))
        self.assertEqual(first.a['href'], '/llms.txt')
        self.assertNotEqual(first.a.get_text(), first.a['href'])

    def test_mermaid_blocks_are_labelled(self):
        soup = self.preprocess('<pre class="mermaid"><code>graph TB</code></pre><pre><code>ls</code></pre>')
        mermaid, other = soup.find_all('pre')
        self.assertEqual(mermaid['class'], ['mermaid', 'language-mermaid'])
        self.assertFalse(other.has_attr('class'))


if __name__ == '__main__':
    unittest.main()
