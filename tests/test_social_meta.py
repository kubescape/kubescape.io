"""Unit tests for the Open Graph and Twitter Card social metadata template."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / 'overrides/main.html'


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

    def test_jinja_rendering_syntax(self):
        try:
            import jinja2
        except ImportError:
            self.skipTest('jinja2 not installed in test environment')

        loader = jinja2.DictLoader({
            'base.html': '<head>{% block extrahead %}<meta name="theme">{% endblock %}</head>',
            'main.html': self.template_content,
        })
        env = jinja2.Environment(loader=loader)
        template = env.get_template('main.html')

        rendered = template.render(
            page=type('Page', (), {
                'title': 'Scanning your cluster',
                'is_homepage': False,
                'meta': {'description': 'Learn how to scan Kubernetes clusters.'},
                'canonical_url': 'https://kubescape.io/docs/scanning/',
            })(),
            config=type('Config', (), {
                'site_name': 'Kubescape',
                'site_url': 'https://kubescape.io/',
                'site_description': 'Kubescape security platform',
            })(),
        )

        self.assertIn('Scanning your cluster - Kubescape', rendered)
        self.assertIn('https://kubescape.io/docs/scanning/', rendered)
        self.assertIn('Learn how to scan Kubernetes clusters.', rendered)
        self.assertIn('https://kubescape.io/assets/kubescape-lockup.svg', rendered)
        self.assertIn('<meta name="theme">', rendered)  # Confirms super() preserved base


if __name__ == '__main__':
    unittest.main()
