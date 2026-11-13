"""Unit tests for the Open Graph and Twitter Card social metadata template."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / 'overrides/main.html'
ASSETS_DIR = ROOT / 'docs/assets'
DEFAULT_IMAGE_NAME = 'kubescape-preview.png'
SUPPORTED_RASTER_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')


class SocialMetadataTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TEMPLATE_PATH.exists(), f"Template not found at {TEMPLATE_PATH}")
        self.template_content = TEMPLATE_PATH.read_text(encoding='utf-8')

    def test_extends_base_html(self):
        self.assertTrue(
            self.template_content.startswith('{% extends "base.html" %}'),
            'Template must extend base.html to inherit theme structure'
        )

    def test_overrides_extrahead_and_calls_super(self):
        self.assertIn('{% block extrahead %}', self.template_content)
        self.assertIn('{{ super() }}', self.template_content)

    def test_contains_essential_open_graph_tags(self):
        expected_og_tags = [
            '<meta property="og:type"',
            '<meta property="og:url"',
            '<meta property="og:title"',
            '<meta property="og:description"',
            '<meta property="og:image"',
            '<meta property="og:site_name"',
        ]
        for tag in expected_og_tags:
            with self.subTest(tag=tag):
                self.assertIn(tag, self.template_content)

    def test_contains_essential_twitter_card_tags(self):
        expected_twitter_tags = [
            '<meta name="twitter:card"',
            '<meta name="twitter:site"',
            '<meta name="twitter:creator"',
            '<meta name="twitter:title"',
            '<meta name="twitter:description"',
            '<meta name="twitter:image"',
        ]
        for tag in expected_twitter_tags:
            with self.subTest(tag=tag):
                self.assertIn(tag, self.template_content)

    def test_default_rendered_image_url_and_raster_format(self):
        """Assert that the default social image fallback is a supported raster format (PNG/JPEG/WebP) and not SVG."""
        try:
            import jinja2
        except ImportError:
            self.skipTest('jinja2 not installed in test environment')

        loader = jinja2.DictLoader({
            'base.html': '<head>{% block extrahead %}{% endblock %}</head>',
            'main.html': self.template_content,
        })
        env = jinja2.Environment(loader=loader)
        template = env.get_template('main.html')

        # Render without page.meta.image (default case for existing pages)
        rendered = template.render(
            page=type('Page', (), {
                'title': 'Getting Started',
                'is_homepage': False,
                'meta': {},
                'canonical_url': 'https://kubescape.io/docs/getting-started/',
            })(),
            config=type('Config', (), {
                'site_name': 'Kubescape',
                'site_url': 'https://kubescape.io/',
                'site_description': 'Kubescape security platform',
            })(),
        )

        # Extract og:image content
        og_match = re.search(r'<meta property="og:image" content="([^"]+)">', rendered)
        self.assertIsNotNone(og_match, 'og:image meta tag not found in rendered output')
        og_image_url = og_match.group(1)

        # Extract twitter:image content
        tw_match = re.search(r'<meta name="twitter:image" content="([^"]+)">', rendered)
        self.assertIsNotNone(tw_match, 'twitter:image meta tag not found in rendered output')
        tw_image_url = tw_match.group(1)

        expected_url = f'https://kubescape.io/assets/{DEFAULT_IMAGE_NAME}'
        self.assertEqual(og_image_url, expected_url)
        self.assertEqual(tw_image_url, expected_url)

        # Ensure format is a supported raster format and NOT SVG
        self.assertFalse(og_image_url.lower().endswith('.svg'), 'Default og:image must not be an SVG')
        self.assertFalse(tw_image_url.lower().endswith('.svg'), 'Default twitter:image must not be an SVG')
        self.assertTrue(
            og_image_url.lower().endswith(SUPPORTED_RASTER_EXTENSIONS),
            f'Default image must be one of {SUPPORTED_RASTER_EXTENSIONS}'
        )

        # Verify the raster asset exists in docs/assets/ and is a valid PNG
        asset_file = ASSETS_DIR / DEFAULT_IMAGE_NAME
        self.assertTrue(asset_file.exists(), f'Asset file does not exist: {asset_file}')
        file_bytes = asset_file.read_bytes()
        self.assertTrue(file_bytes.startswith(b'\x89PNG\r\n\x1a\n'), 'Asset file is not a valid PNG')

    def test_custom_page_image_override(self):
        """Verify that a page with page.meta.image overrides the default fallback."""
        try:
            import jinja2
        except ImportError:
            self.skipTest('jinja2 not installed in test environment')

        loader = jinja2.DictLoader({
            'base.html': '<head>{% block extrahead %}{% endblock %}</head>',
            'main.html': self.template_content,
        })
        env = jinja2.Environment(loader=loader)
        template = env.get_template('main.html')

        rendered = template.render(
            page=type('Page', (), {
                'title': 'Blog Post',
                'is_homepage': False,
                'meta': {'image': 'blog/posts/custom-hero.png'},
                'canonical_url': 'https://kubescape.io/blog/posts/custom-hero/',
            })(),
            config=type('Config', (), {
                'site_name': 'Kubescape',
                'site_url': 'https://kubescape.io/',
                'site_description': 'Kubescape security platform',
            })(),
        )

        self.assertIn('https://kubescape.io/blog/posts/custom-hero.png', rendered)


if __name__ == '__main__':
    unittest.main()
