"""Unit tests for the control explorer card generator and synchronizer."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_control_index.py"
REPO_ROOT = Path(__file__).resolve().parents[1]


class ControlIndexGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.controls_dir = self.root / "controls"
        self.controls_dir.mkdir(parents=True)
        self.index_file = self.controls_dir / "index.md"
        self.metadata_file = self.root / "control_metadata.json"
        self.metadata_file.write_text("{}", encoding="utf-8")

    def write_index(self, cards_content: str = ""):
        content = (
            "# Control library\n\n"
            '<div class="ks-control-explorer" id="ks-control-explorer"></div>\n\n'
            '<div class="ks-controls-grid" id="ks-controls-grid">\n'
            "<!-- ks:controls:cards:start -->\n"
            f"{cards_content}\n"
            "<!-- ks:controls:cards:end -->\n"
            "</div>\n\n"
            '<div id="ks-no-results" class="ks-no-results" style="display:none;"></div>\n'
        )
        self.index_file.write_text(content, encoding="utf-8")

    def write_control(self, filename: str, title: str = "Test Control", severity: str = "High", category: str | None = "container"):
        content = (
            f"# {filename[:6].upper()} - {title}\n\n"
            "[← Back to all controls](index.md)\n\n"
            f"## Severity\n\n{severity}\n\n"
            "## Description of the the issue\n\nTest description.\n"
        )
        if category is not None:
            metadata = json.loads(self.metadata_file.read_text())
            metadata[Path(filename).stem.upper()] = {"category": category}
            self.metadata_file.write_text(json.dumps(metadata))
        path = self.controls_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

    def run_script(self, *extra_args):
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--controls-dir",
            str(self.controls_dir),
            "--index-file",
            str(self.index_file),
            "--metadata-file",
            str(self.metadata_file),
            *extra_args,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def test_repo_controls_are_in_sync(self):
        """Verify that the repository's control index.md is currently 100% in sync."""
        cmd = [sys.executable, str(SCRIPT), "--check"]
        result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Sync check failed:\n{result.stderr}\n{result.stdout}")
        self.assertIn("fully in sync", result.stdout)

    def test_sync_generates_valid_cards(self):
        self.write_control("c-0001.md", title="Forbidden Registries", severity="High")
        self.write_index()

        code, stdout, stderr = self.run_script()
        self.assertEqual(code, 0)
        self.assertIn("Successfully synchronized 1 control cards", stdout)

        updated_index = self.index_file.read_text(encoding="utf-8")
        self.assertIn('data-id="C-0001"', updated_index)
        self.assertIn('data-sev="high"', updated_index)
        self.assertIn("Forbidden Registries", updated_index)
        self.assertIn("kubescape scan control C-0001", updated_index)

    def test_check_fails_when_severity_differs(self):
        self.write_control("c-0001.md", title="Forbidden Registries", severity="Critical")
        self.write_index(
            '  <div class="ks-control-card" data-id="C-0001" data-sev="low" data-cat="container">\n'
            '    <div class="ks-card-header">\n'
            '      <a class="ks-card-id" href="c-0001/">C-0001</a>\n'
            '      <span class="ks-badge ks-badge-low">Low</span>\n'
            "    </div>\n"
            '    <a class="ks-card-title" href="c-0001/">Forbidden Registries</a>\n'
            '    <div class="ks-card-footer">\n'
            '      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0001">📋 Copy scan command</button>\n'
            "    </div>\n"
            "  </div>"
        )

        code, stdout, stderr = self.run_script("--check")
        self.assertEqual(code, 1)
        self.assertIn("out of sync", stderr)

    def test_check_fails_when_title_differs(self):
        self.write_control("c-0001.md", title="New Control Title", severity="High")
        self.write_index(
            '  <div class="ks-control-card" data-id="C-0001" data-sev="high" data-cat="container">\n'
            '    <div class="ks-card-header">\n'
            '      <a class="ks-card-id" href="c-0001/">C-0001</a>\n'
            '      <span class="ks-badge ks-badge-high">High</span>\n'
            "    </div>\n"
            '    <a class="ks-card-title" href="c-0001/">Old Control Title</a>\n'
            '    <div class="ks-card-footer">\n'
            '      <button type="button" class="ks-copy-cmd-btn" data-cmd="kubescape scan control C-0001">📋 Copy scan command</button>\n'
            "    </div>\n"
            "  </div>"
        )

        code, stdout, stderr = self.run_script("--check")
        self.assertEqual(code, 1)
        self.assertIn("out of sync", stderr)

    def test_title_is_rendered_as_literal_text(self):
        self.write_index()
        self.write_control("c-0001.md", title=r"Compare <limit> & \1")
        self.assertEqual(self.run_script()[0], 0)
        self.assertIn(r"Compare &lt;limit&gt; &amp; \1</a>", self.index_file.read_text())
        self.assertEqual(self.run_script("--check")[0], 0)

    def test_missing_or_invalid_category_leaves_index_intact(self):
        self.write_index()
        original = self.index_file.read_bytes()
        for category in (None, "unknown"):
            self.write_control("c-0001.md", title="Check RBAC tokens", category=category)
            for args in ((), ("--check",)):
                with self.subTest(category=category, args=args):
                    code, _, stderr = self.run_script(*args)
                    self.assertEqual(code, 1)
                    self.assertIn("C-0001: missing or invalid category", stderr)
                    self.assertEqual(self.index_file.read_bytes(), original)

    def test_missing_directory_returns_error(self):
        code, stdout, stderr = self.run_script("--controls-dir", str(self.root / "nonexistent"))
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
