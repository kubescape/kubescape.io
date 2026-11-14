"""Exercise the link checker's command-line and report contract."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import socket
import sys
import tempfile
import threading
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_links.py'


class InternalLinksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.site = self.root / 'site'
        self.report = self.root / 'report.json'
        self.inventory = self.root / 'inventory.json'
        self.inventory.write_text('{"examples": [], "exceptions": []}')

    def write(self, name, content):
        path = self.site / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def check(self, mode='internal', *options):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), mode, '--site-dir', str(self.site),
             '--site-url', 'https://kubescape.io/', '--inventory', str(self.inventory),
             '--report', str(self.report), *options], capture_output=True, text=True)
        self.assertTrue(self.report.exists(), result.stderr)
        return result.returncode, json.loads(self.report.read_text())

    def test_missing_or_empty_site_is_incomplete(self):
        for create_directory in (False, True):
            if create_directory:
                self.site.mkdir()
            with self.subTest(empty=create_directory):
                code, report = self.check()
                self.assertEqual(code, 2)
                self.assertFalse(report['complete'])
                self.assertTrue(report['errors'])
                self.assertEqual(report['counts']['pages'], 0)

    def test_missing_page_anchor_and_resource_fail(self):
        self.write('index.html', '<a href="missing/">Page</a><a href="ok/#absent">Section</a><img src="missing.png">')
        self.write('ok/index.html', '<h1 id="present">Present</h1>')
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertTrue(report['complete'])
        self.assertEqual(report['counts']['pages'], 2)
        self.assertCountEqual([f['kind'] for f in report['failures']], ['missing_file', 'missing_file', 'missing_anchor'])
        self.assertEqual(report['counts']['failures'], 3)
        self.assertTrue(all(f['source'] and f['url'] and f['resolved_url'] for f in report['failures']))

    def test_paths_queries_fragments_css_and_srcset(self):
        self.write('index.html', '''<a href="guide/#a%2Bb">One</a>
            <a href="https://www.kubescape.io/guide/?source=test#a+b">Two</a>
            <link rel="stylesheet" href="assets/style.css?v=2">
            <picture><source srcset="data:image/png;base64,aGVsbG8= 1x, assets/photo.png 2x"></picture>''')
        self.write('guide/index.html', '<h1 id="a+b">Heading</h1><a href="../#">Home</a>')
        self.write('assets/style.css', '@import "more.css"; body {background: url(../photo.svg?version=1)}')
        self.write('assets/more.css', '')
        self.write('assets/photo.png', 'image')
        self.write('photo.svg', '<svg/>')
        code, report = self.check()
        self.assertEqual(code, 0)
        self.assertEqual(report['counts']['internal_references'], 7)
        self.assertEqual(report['counts']['skipped_non_http'], 1)
        (self.site / 'photo.svg').unlink()
        (self.site / 'assets/photo.png').unlink()
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertCountEqual([f['target'] for f in report['failures']], ['photo.svg', 'assets/photo.png'])
        (self.site / 'assets/more.css').unlink()
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertIn('assets/more.css', [f['target'] for f in report['failures']])

    def test_llms_txt_and_markdown_copies(self):
        self.write('index.html', '<h1>Home</h1>')
        self.write('guide/index.html', '<h1 id="install">Install</h1>')
        self.write('llms.txt', '# Kubescape\n\n> Summary\n\n## Docs\n\n- [Guide](https://kubescape.io/guide/index.md)\n')
        self.write('guide/index.md', 'Index at [llms.txt](/llms.txt). See [install](https://kubescape.io/guide/#install).\n\n'
                                     '```markdown\n[example](missing/)\n```\n')
        code, report = self.check()
        self.assertEqual(code, 0)
        self.assertEqual(report['counts']['internal_references'], 3)
        (self.site / 'guide/index.md').write_text('[Missing](https://kubescape.io/gone/index.md) [Anchor](../#absent)')
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertCountEqual([(f['source'], f['kind']) for f in report['failures']],
                              [('guide/index.md', 'missing_file'), ('guide/index.md', 'missing_anchor')])

    def test_exception_matches_both_source_and_exact_url(self):
        self.write('index.html', '<a href="missing/">Intentional example</a>')
        self.write('other/index.html', '<a href="../missing/">Unintentional</a>')
        self.inventory.write_text(json.dumps({'examples': [], 'exceptions': [
            {'source': 'index.html', 'url': 'missing/', 'reason': 'Fixture example'}]}))
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertEqual(len(report['exceptions']), 1)
        self.assertEqual(len(report['failures']), 1)

    def test_invalid_inventory_and_unreadable_html_are_incomplete(self):
        self.write('index.html', '<h1>Page</h1>')
        self.inventory.write_text('{"examples": "not an array", "exceptions": []}')
        code, report = self.check()
        self.assertEqual(code, 2)
        self.assertFalse(report['complete'])
        self.inventory.write_text('{"examples": [], "exceptions": []}')
        (self.site / 'index.html').write_bytes(b'\xff')
        code, report = self.check()
        self.assertEqual(code, 2)
        self.assertFalse(report['complete'])

    def test_invalid_url_and_arguments_preserve_incomplete_reports(self):
        self.write('index.html', '<a href="https://kubescape.io:bad/">Invalid port</a>')
        code, report = self.check()
        self.assertEqual(code, 2)
        self.assertFalse(report['complete'])
        self.assertTrue(report['errors'])
        code, report = self.check('internal', '--unknown-option')
        self.assertEqual(code, 2)
        self.assertFalse(report['complete'])

    def test_nondefault_port_is_external_and_examples_require_absolute_urls(self):
        self.write('index.html', '<a href="https://kubescape.io:8443/">Other origin</a>')
        code, report = self.check()
        self.assertEqual(code, 0)
        self.assertEqual(report['counts']['internal_references'], 0)
        self.assertEqual(report['counts']['external_references'], 1)
        for url in ('missing.yaml', 'https://', 'https://example.org:bad/file.yaml'):
            self.inventory.write_text(json.dumps({'examples': [
                {'source': 'guide.md', 'url': url, 'reason': 'Example'}], 'exceptions': []}))
            code, report = self.check()
            self.assertEqual(code, 2, url)
            self.assertFalse(report['complete'])


class ExternalLinksTest(unittest.TestCase):
    setUp = InternalLinksTest.setUp
    write = InternalLinksTest.write
    check = InternalLinksTest.check

    @classmethod
    def setUpClass(cls):
        class Handler(BaseHTTPRequestHandler):
            retry_count = 0

            def log_message(self, *args):
                pass

            def do_GET(self):
                status = {'/private': 401, '/forbidden': 403, '/rate': 429, '/gone': 404}.get(self.path, 200)
                if self.path == '/slow':
                    time.sleep(1)
                if self.path == '/retry':
                    Handler.retry_count += 1
                    status = 503 if Handler.retry_count == 1 else 200
                redirects = {'/redirect': '/landing', '/loop': '/loop',
                             '/redirect-fragment': '/landing#present', '/redirect-clear': '/landing#'}
                self.send_response(302 if self.path in redirects else status)
                if self.path in redirects:
                    self.send_header('Location', redirects[self.path])
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                try:
                    self.wfile.write(b'<title>Unrelated landing</title><h1 id="present">Page</h1>')
                except BrokenPipeError:
                    pass

        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)

    def test_external_findings_are_advisory_and_redirects_remain_visible(self):
        paths = ['/ok#present', '/ok#absent', '/private', '/forbidden', '/rate', '/gone', '/redirect', '/loop', '/slow']
        self.write('index.html', ''.join(f'<a href="{self.base}{path}">Link</a>' for path in paths))
        code, report = self.check('external', '--timeout', '0.5', '--retries', '0')
        self.assertEqual(code, 0)
        self.assertTrue(report['complete'])
        results = {r['url'].removeprefix(self.base): r for r in report['external_results']}
        expected = {'/ok#present': 'reachable', '/ok#absent': 'missing_anchor', '/private': 'access_denied',
                    '/forbidden': 'access_denied', '/rate': 'rate_limited', '/gone': 'not_found',
                    '/redirect': 'reachable', '/loop': 'redirect_limit', '/slow': 'timeout'}
        self.assertEqual({path: result['kind'] for path, result in results.items()}, expected)
        self.assertEqual(results['/redirect']['final_url'], self.base + '/landing')
        self.assertEqual(results['/redirect']['redirects'][0]['status'], 302)
        self.assertEqual(results['/redirect']['title'], 'Unrelated landing')
        self.assertEqual(report['counts']['external_requests'], 8)
        self.assertEqual(report['counts']['failures'], 2)
        self.assertEqual(report['counts']['unverified'], 5)

    def test_transient_failure_is_retried_and_inventory_is_checked(self):
        self.write('index.html', '<h1>Page</h1>')
        self.inventory.write_text(json.dumps({'examples': [
            {'source': 'guide.md', 'url': self.base + '/retry', 'reason': 'Static example'}], 'exceptions': []}))
        code, report = self.check('external', '--retries', '1')
        self.assertEqual(code, 0)
        result = report['external_results'][0]
        self.assertEqual(result['kind'], 'reachable')
        self.assertEqual(result['attempts'], 2)
        self.assertEqual(result['references'][0]['source'], 'guide.md')

    def test_redirects_override_clear_or_inherit_fragments(self):
        paths = ['/redirect-fragment#absent', '/redirect-clear#absent', '/redirect#present', '/redirect#absent']
        self.write('index.html', ''.join(f'<a href="{self.base}{path}">Link</a>' for path in paths))
        code, report = self.check('external')
        self.assertEqual(code, 0)
        results = {r['url'].removeprefix(self.base): r for r in report['external_results']}
        self.assertEqual(results['/redirect-fragment#absent']['kind'], 'reachable')
        self.assertEqual(results['/redirect-clear#absent']['kind'], 'reachable')
        self.assertEqual(results['/redirect#present']['kind'], 'reachable')
        self.assertEqual(results['/redirect#absent']['kind'], 'missing_anchor')

    def test_fragment_exception_still_checks_availability(self):
        url = self.base + '/ok#/app-route'
        self.write('index.html', f'<a href="{url}">Application</a>')
        self.inventory.write_text(json.dumps({'examples': [], 'exceptions': [
            {'source': 'index.html', 'url': url, 'reason': 'Client-side route', 'fragment_only': True}]}))
        code, report = self.check('external')
        self.assertEqual(code, 0)
        self.assertEqual(report['counts']['external_requests'], 1)
        self.assertEqual(report['external_results'][0]['status'], 200)
        self.assertEqual(report['external_results'][0]['kind'], 'fragment_unverified')
        self.assertEqual(len(report['exceptions']), 1)

    def test_network_failure_is_unverified_not_an_incomplete_scan(self):
        with socket.socket() as unavailable:
            unavailable.bind(('127.0.0.1', 0))
            url = f'http://127.0.0.1:{unavailable.getsockname()[1]}/'
            self.write('index.html', f'<a href="{url}">Unavailable</a>')
            code, report = self.check('external', '--retries', '0')
        self.assertEqual(code, 0)
        self.assertTrue(report['complete'])
        self.assertEqual(report['unverified'][0]['kind'], 'network_error')
        self.assertEqual(report['failures'], [])

    def test_missing_site_and_bad_config_are_incomplete_in_external_mode(self):
        code, report = self.check('external')
        self.assertEqual(code, 2)
        self.assertFalse(report['complete'])
        self.write('index.html', '<h1>Page</h1>')
        self.inventory.write_text('{broken json')
        code, report = self.check('external')
        self.assertEqual(code, 2)
        self.assertFalse(report['complete'])

    def test_in_progress_report_survives_process_termination(self):
        self.write('index.html', f'<a href="{self.base}/slow">Slow</a>')
        process = subprocess.Popen([sys.executable, '-B', str(SCRIPT), 'external',
            '--site-dir', str(self.site), '--inventory', str(self.inventory),
            '--report', str(self.report)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        self.addCleanup(lambda: process.poll() is None and process.kill())
        deadline = time.monotonic() + 5
        while not self.report.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.005)
        self.assertTrue(self.report.exists())
        process.terminate()
        process.communicate(timeout=5)
        self.assertFalse(json.loads(self.report.read_text())['complete'])


if __name__ == '__main__':
    unittest.main()
