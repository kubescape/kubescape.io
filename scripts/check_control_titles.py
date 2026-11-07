#!/usr/bin/env python3
"""Check that control reference pages have descriptive HTML and source titles."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

DEFAULT_CONTROLS_DIR = Path(__file__).resolve().parents[1] / 'docs/docs/controls'


class TitleH1Parser(HTMLParser):
    """Extract <title> and first <h1> text from rendered HTML."""

    def __init__(self):
        super().__init__()
        self.title = None
        self.h1 = None
        self._in_title = False
        self._in_h1 = False
        self._title_parts = []
        self._h1_parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'title' and self.title is None:
            self._in_title = True
        elif tag == 'h1' and self.h1 is None:
            self._in_h1 = True

    def handle_endtag(self, tag):
        if tag == 'title' and self._in_title:
            self._in_title = False
            self.title = ''.join(self._title_parts).strip()
        elif tag == 'h1' and self._in_h1:
            self._in_h1 = False
            self.h1 = ''.join(self._h1_parts).strip()

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)
        elif self._in_h1:
            self._h1_parts.append(data)


def parse_source_control(markdown_path: Path):
    """Parse Markdown source for frontmatter title, first H1, and backlink position."""
    content = markdown_path.read_text(encoding='utf-8')
    lines = content.splitlines()

    frontmatter_title = None
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                break
            if lines[i].startswith('title:'):
                frontmatter_title = lines[i].split('title:', 1)[1].strip().strip('"\'')

    h1_line = None
    h1_index = None
    backlink_index = None

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if 'Back to all controls' in stripped and backlink_index is None:
            backlink_index = idx
        if stripped.startswith('# ') and h1_line is None:
            clean_h1 = re.sub(r'\s*\{#.*\}\s*$', '', stripped[2:]).strip()
            h1_line = clean_h1
            h1_index = idx

    has_backlink_before_h1 = (
        backlink_index is not None and h1_index is not None and backlink_index < h1_index
    )

    return {
        'path': str(markdown_path),
        'file': markdown_path.name,
        'frontmatter_title': frontmatter_title,
        'h1': h1_line,
        'has_descriptive_h1': bool(h1_line and len(h1_line.split('-', 1)) > 1),
        'backlink_before_h1': has_backlink_before_h1,
    }


def check_rendered_site(site_dir: Path, controls_info: dict):
    """Check rendered HTML files against source expectations."""
    findings = []
    checked = 0

    controls_site = site_dir / 'docs/controls'
    if not controls_site.exists():
        controls_site = site_dir / 'controls'
    if not controls_site.exists():
        return {
            'complete': False,
            'error': f"Controls directory not found in site: {site_dir}",
            'checked': 0,
            'findings': [],
        }

    for html_path in sorted(controls_site.glob('c-*/index.html')):
        control_id = html_path.parent.name
        src_file = f"{control_id}.md"
        src_info = controls_info.get(src_file)

        parser = TitleH1Parser()
        parser.feed(html_path.read_text(encoding='utf-8'))
        title = parser.title or ''
        checked += 1

        expected_title_part = (
            src_info.get('frontmatter_title')
            or (src_info.get('h1') if src_info and src_info.get('has_descriptive_h1') else None)
        )

        if expected_title_part:
            clean_expected = expected_title_part.split(' - ', 1)[-1].strip()
            if clean_expected not in title:
                findings.append({
                    'control': control_id,
                    'html_file': str(html_path),
                    'title': title,
                    'expected': expected_title_part,
                    'reason': 'Rendered title misses descriptive control heading',
                })

    return {
        'complete': True,
        'checked': checked,
        'findings': findings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls-dir', type=Path, default=DEFAULT_CONTROLS_DIR,
                        help='Path to source controls markdown directory')
    parser.add_argument('--site-dir', type=Path, default=None,
                        help='Path to rendered MkDocs site directory')
    parser.add_argument('--report', type=Path, default=None,
                        help='Path to output JSON report')
    args = parser.parse_args(argv)

    if not args.controls_dir.exists():
        sys.stderr.write(f"Error: controls directory not found: {args.controls_dir}\n")
        return 2

    sources = {}
    source_order_failures = []
    for md_file in sorted(args.controls_dir.glob('c-*.md')):
        info = parse_source_control(md_file)
        sources[md_file.name] = info
        if info['backlink_before_h1'] and info['has_descriptive_h1']:
            source_order_failures.append({
                'file': md_file.name,
                'path': str(md_file),
                'h1': info['h1'],
                'reason': 'Back-link precedes descriptive H1 heading',
            })

    rendered_result = None
    if args.site_dir:
        if not args.site_dir.exists():
            sys.stderr.write(f"Error: site directory not found: {args.site_dir}\n")
            return 2
        rendered_result = check_rendered_site(args.site_dir, sources)
        if not rendered_result['complete']:
            sys.stderr.write(f"Error: {rendered_result['error']}\n")
            return 2

    rendered_findings = rendered_result['findings'] if rendered_result else []
    total_failures = len(source_order_failures) + len(rendered_findings)

    report_data = {
        'controls_scanned': len(sources),
        'descriptive_headings_found': sum(1 for s in sources.values() if s['has_descriptive_h1']),
        'source_order_failures': source_order_failures,
        'rendered_site_checked': bool(args.site_dir),
        'rendered_findings': rendered_findings,
        'passed': total_failures == 0,
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report_data, indent=2) + '\n', encoding='utf-8')

    if total_failures > 0:
        print(f"FAILED: Found {len(source_order_failures)} source ordering defects "
              f"and {len(rendered_findings)} rendered title defects.")
        for f in source_order_failures:
            print(f"  [Source Order] {f['file']}: {f['reason']} (H1: {f['h1']})")
        for f in rendered_findings:
            print(f"  [Rendered Title] {f['control']}: {f['reason']} "
                  f"(Got: '{f['title']}', Expected: '{f['expected']}')")
        return 1

    print(f"SUCCESS: Checked {len(sources)} controls ({report_data['descriptive_headings_found']} descriptive). "
          f"All title hierarchies and ordering are correct.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
