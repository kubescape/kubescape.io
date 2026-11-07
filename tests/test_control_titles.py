"""Unit tests for the control titles integrity checker."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_control_titles.py'


class ControlTitlesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.controls_dir = self.root / 'controls'
        self.controls_dir.mkdir(parents=True)
        self.report = self.root / 'report.json'

    def write_control(self, filename: str, content: str):
        path = self.controls_dir / filename
        path.write_text(content, encoding='utf-8')
        return path

    def run_check(self, *extra_args):
        cmd = [
            sys.executable,
            str(SCRIPT),
            '--controls-dir',
            str(self.controls_dir),
            '--report',
            str(self.report),
            *extra_args,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        report_data = json.loads(self.report.read_text(encoding='utf-8')) if self.report.exists() else None
        return result.returncode, result.stdout, result.stderr, report_data

    def test_heading_first_passes(self):
        self.write_control(
            'c-0066.md',
            '# C-0066 - Secret/etcd encryption enabled\n\n'
            '[← Back to all controls](index.md)\n\n'
            '## Severity\nHigh\n'
        )
        code, stdout, stderr, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertTrue(report['passed'])
        self.assertEqual(len(report['source_order_failures']), 0)
        self.assertEqual(report['descriptive_headings_found'], 1)

    def test_backlink_first_fails_when_descriptive_h1_exists(self):
        self.write_control(
            'c-0005.md',
            '[← Back to all controls](index.md)\n\n'
            '# C-0005 - API server insecure port is enabled\n\n'
            '## Severity\nMedium\n'
        )
        code, stdout, stderr, report = self.run_check()
        self.assertEqual(code, 1)
        self.assertFalse(report['passed'])
        self.assertEqual(len(report['source_order_failures']), 1)
        self.assertEqual(report['source_order_failures'][0]['file'], 'c-0005.md')

    def test_control_without_descriptive_h1_does_not_fail_unjustly(self):
        # 193 controls lack a descriptive name; they should not block the build
        self.write_control(
            'c-0074.md',
            '[← Back to all controls](index.md)\n\n'
            'AllControls, DevOpsBest, security\n\n'
            '## Severity\nMedium\n'
        )
        code, stdout, stderr, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertTrue(report['passed'])
        self.assertEqual(len(report['source_order_failures']), 0)
        self.assertEqual(report['descriptive_headings_found'], 0)

    def test_explicit_anchor_and_frontmatter_title_handled(self):
        self.write_control(
            'c-0001.md',
            '---\n'
            'title: "C-0001 - Forbidden Container Registries"\n'
            '---\n\n'
            '# C-0001 - Forbidden Container Registries {#custom-anchor}\n\n'
            '[← Back to all controls](index.md)\n'
        )
        code, stdout, stderr, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertTrue(report['passed'])

    def test_missing_controls_dir_returns_code_2(self):
        cmd = [sys.executable, str(SCRIPT), '--controls-dir', str(self.root / 'nonexistent')]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
