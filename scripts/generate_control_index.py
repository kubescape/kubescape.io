#!/usr/bin/env python3
"""Generate and synchronize Kubescape control explorer cards from control metadata.

This script parses individual control markdown files (docs/docs/controls/c-*.md)
to extract severities and titles directly from source files, combines them with
category metadata, and generates the interactive cards grid in
docs/docs/controls/index.md.
"""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTROLS_DIR = REPO_ROOT / "docs" / "docs" / "controls"
DEFAULT_INDEX_FILE = DEFAULT_CONTROLS_DIR / "index.md"
DEFAULT_METADATA_FILE = REPO_ROOT / "scripts" / "control_metadata.json"

START_MARKER = "<!-- ks:controls:cards:start -->"
END_MARKER = "<!-- ks:controls:cards:end -->"

VALID_SEVERITIES = {"critical", "high", "medium", "low"}
VALID_CATEGORIES = {"container", "rbac", "network", "cluster"}


def parse_control_file(file_path: Path, metadata_lookup: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Extract control ID, title, severity, and category from a control markdown file."""
    control_id = file_path.stem.upper()
    link_path = f"{file_path.stem.lower()}/"
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    fallback_info = (metadata_lookup or {}).get(control_id, {})

    # 1. Parse frontmatter if present
    frontmatter_title = None
    frontmatter_category = None
    frontmatter_severity = None

    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            line = lines[idx].strip()
            if line == "---":
                break
            if line.startswith("title:"):
                frontmatter_title = line.split("title:", 1)[1].strip().strip('"\'')
            elif line.startswith("category:"):
                frontmatter_category = line.split("category:", 1)[1].strip().strip('"\'').lower()
            elif line.startswith("severity:"):
                frontmatter_severity = line.split("severity:", 1)[1].strip().strip('"\'').lower()

    # 2. Parse title
    title = frontmatter_title
    if not title:
        in_code_block = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if stripped.startswith("# "):
                clean = re.sub(r"\s*\{#.*\}\s*$", "", stripped[2:]).strip()
                # Check for standard '# C-XXXX - Title' pattern
                prefix = f"{control_id} - "
                if clean.upper().startswith(prefix):
                    title = clean[len(prefix):].strip()
                    break
                elif " - " in clean and clean.split(" - ", 1)[0].strip().upper() == control_id:
                    title = clean.split(" - ", 1)[1].strip()
                    break

    if not title:
        title = fallback_info.get("title") or control_id

    # 3. Parse severity directly from ## Severity
    severity = frontmatter_severity
    if not severity:
        for idx, line in enumerate(lines):
            if line.strip().lower() == "## severity":
                for next_idx in range(idx + 1, min(idx + 10, len(lines))):
                    candidate = lines[next_idx].strip()
                    if candidate:
                        severity = candidate.lower()
                        break
                break

    if not severity or severity not in VALID_SEVERITIES:
        severity = (fallback_info.get("severity") or "medium").lower()

    # 4. Parse category
    category = frontmatter_category
    if not category:
        category = (fallback_info.get("category") or "").lower()

    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"{control_id}: missing or invalid category {category!r}. "
            f"Set category in frontmatter or control metadata to one of: {', '.join(sorted(VALID_CATEGORIES))}."
        )

    return {
        "id": control_id,
        "title": title,
        "severity": severity,
        "severity_display": severity.capitalize(),
        "category": category,
        "link": link_path,
        "cmd": f"kubescape scan control {control_id}",
    }


def render_card(control: dict[str, Any]) -> str:
    """Render HTML for a single control card."""
    return (
        f'  <div class="ks-control-card" data-id="{control["id"]}" data-sev="{control["severity"]}" data-cat="{control["category"]}">\n'
        f'    <div class="ks-card-header">\n'
        f'      <a class="ks-card-id" href="{control["link"]}">{control["id"]}</a>\n'
        f'      <span class="ks-badge ks-badge-{control["severity"]}">{control["severity_display"]}</span>\n'
        f'    </div>\n'
        f'    <a class="ks-card-title" href="{control["link"]}">{escape(control["title"])}</a>\n'
        f'    <div class="ks-card-footer">\n'
        f'      <button type="button" class="ks-copy-cmd-btn" data-cmd="{control["cmd"]}" title="Copy scan command">📋 Copy scan command</button>\n'
        f'    </div>\n'
        f'  </div>'
    )


def generate_cards_html(controls: list[dict[str, Any]]) -> str:
    """Generate all cards wrapped inside start and end markers."""
    cards_str = "\n".join(render_card(c) for c in controls)
    return f"{START_MARKER}\n\n{cards_str}\n\n{END_MARKER}"


def update_index_content(existing_text: str, new_cards_block: str) -> str:
    """Inject generated cards block into index.md markdown content."""
    # If markers exist, replace between them
    if START_MARKER in existing_text and END_MARKER in existing_text:
        pattern = re.compile(
            rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
            re.DOTALL,
        )
        return pattern.sub(lambda _: new_cards_block, existing_text)

    # If markers do not exist yet, inject inside <div class="ks-controls-grid" id="ks-controls-grid">
    grid_start_tag = '<div class="ks-controls-grid" id="ks-controls-grid">'
    grid_pos = existing_text.find(grid_start_tag)
    if grid_pos != -1:
        after_grid = grid_pos + len(grid_start_tag)
        # Find closing tag of this grid container
        # Next top-level </div> followed by no-results or empty line
        closing_div_pos = existing_text.find("</div>\n\n<div id=\"ks-no-results\"", after_grid)
        if closing_div_pos != -1:
            return (
                existing_text[:after_grid]
                + "\n\n"
                + new_cards_block
                + "\n"
                + existing_text[closing_div_pos:]
            )

    raise ValueError("Could not find <div class=\"ks-controls-grid\" id=\"ks-controls-grid\"> in index.md")


def sync_controls(
    controls_dir: Path = DEFAULT_CONTROLS_DIR,
    index_file: Path = DEFAULT_INDEX_FILE,
    metadata_file: Path = DEFAULT_METADATA_FILE,
    check_only: bool = False,
) -> tuple[bool, str]:
    """Synchronize or verify controls cards in index.md. Returns (in_sync, message)."""
    if not controls_dir.exists():
        return False, f"Controls directory not found: {controls_dir}"
    if not index_file.exists():
        return False, f"Index file not found: {index_file}"

    metadata_lookup = {}
    if metadata_file.exists():
        try:
            metadata_lookup = json.loads(metadata_file.read_text(encoding="utf-8"))
        except Exception as e:
            return False, f"Error reading metadata file {metadata_file}: {e}"

    control_files = sorted(controls_dir.glob("c-*.md"))
    if not control_files:
        return False, f"No control files found in {controls_dir}"

    try:
        controls = [parse_control_file(f, metadata_lookup) for f in control_files]
    except ValueError as exc:
        return False, str(exc)
    new_cards_block = generate_cards_html(controls)

    current_index_text = index_file.read_text(encoding="utf-8")
    updated_index_text = update_index_content(current_index_text, new_cards_block)

    is_identical = (current_index_text == updated_index_text)

    if check_only:
        if is_identical:
            return True, f"Control cards in {index_file} are fully in sync ({len(controls)} controls)."
        return False, f"Control cards in {index_file} are out of sync with control source files."

    if not is_identical:
        index_file.write_text(updated_index_text, encoding="utf-8")
        return True, f"Successfully synchronized {len(controls)} control cards in {index_file}."

    return True, f"Control cards in {index_file} were already up to date ({len(controls)} controls)."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls-dir", type=Path, default=DEFAULT_CONTROLS_DIR,
                        help="Path to control markdown directory")
    parser.add_argument("--index-file", type=Path, default=DEFAULT_INDEX_FILE,
                        help="Path to controls index.md")
    parser.add_argument("--metadata-file", type=Path, default=DEFAULT_METADATA_FILE,
                        help="Path to control metadata JSON")
    parser.add_argument("--check", action="store_true",
                        help="Check if index.md is in sync without modifying it")
    args = parser.parse_args(argv)

    success, message = sync_controls(
        controls_dir=args.controls_dir,
        index_file=args.index_file,
        metadata_file=args.metadata_file,
        check_only=args.check,
    )

    if not success:
        print(f"FAILED: {message}", file=sys.stderr)
        return 1

    print(f"SUCCESS: {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
