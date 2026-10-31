#!/usr/bin/env python3
"""Check a rendered MkDocs site. External checks report availability, not correctness."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEFAULT_INVENTORY = Path(__file__).with_name('linkcheck-inventory.json')
CSS_URL = re.compile(r'''url\(\s*(?:"([^"]*)"|'([^']*)'|([^\s)]*))\s*\)|@import\s+(?:"([^"]*)"|'([^']*)')''', re.IGNORECASE)
MARKDOWN_FENCE = re.compile(r'^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$', re.MULTILINE | re.DOTALL)
MARKDOWN_LINK = re.compile(r'\]\(\s*<?([^)\s>]+)')


def css_urls(text):
    """Extract static CSS resources, not computed CSS or JavaScript expressions."""
    for match in CSS_URL.finditer(re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)):
        url = next(group for group in match.groups() if group is not None)
        if '\\' in url:
            raise ValueError('Escaped CSS URLs are unsupported; coverage would be incomplete')
        yield url


def markdown_urls(text):
    """Extract inline link targets from generated Markdown (llms.txt and page copies), outside fenced code."""
    for match in MARKDOWN_LINK.finditer(MARKDOWN_FENCE.sub('', text)):
        yield match.group(1)


def srcset_urls(value):
    """Read URL tokens before descriptors; commas inside data URLs are not separators."""
    position = 0
    while position < len(value):
        while position < len(value) and (value[position].isspace() or value[position] == ','):
            position += 1
        start = position
        while position < len(value) and not value[position].isspace():
            position += 1
        token = value[start:position]
        if not token:
            break
        yield token.rstrip(',')
        if token.endswith(','):
            continue
        # Descriptors end at a comma, except within parentheses.
        depth = 0
        while position < len(value):
            character = value[position]
            position += 1
            depth += (character == '(') - (character == ')')
            if character == ',' and depth == 0:
                break


class Page(HTMLParser):
    def __init__(self, text, collect_resources=True):
        super().__init__(convert_charrefs=True)
        self.anchors = set()
        self.references = []
        self.base = None
        self.in_style = False
        self.in_title = False
        self.title = ''
        self.collect_resources = collect_resources
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == 'title':
            self.in_title = True
        if tag == 'base':
            if self.base is None:
                self.base = attributes.get('href')
            return
        if tag == 'style':
            self.in_style = True
        if attributes.get('id'):
            self.anchors.add(attributes['id'])
        if tag == 'a' and attributes.get('name'):
            self.anchors.add(attributes['name'])
        if not self.collect_resources:
            return
        if tag == 'link' and set(attributes.get('rel', '').split()) & {'preconnect', 'dns-prefetch'}:
            return
        for attribute in ('href', 'src', 'poster'):
            if attributes.get(attribute):
                self.references.append((attribute, attributes[attribute]))
        if attributes.get('srcset'):
            self.references.extend(('srcset', url) for url in srcset_urls(attributes['srcset']))
        if attributes.get('style'):
            self.references.extend(('style', url) for url in css_urls(attributes['style']))

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_style and self.collect_resources:
            self.references.extend(('style', url) for url in css_urls(data))


def load_inventory(path):
    inventory = json.loads(path.read_text(encoding='utf-8'))
    for key in ('examples', 'exceptions'):
        if not isinstance(inventory.get(key), list):
            raise ValueError(f'Inventory must contain a {key} array')
        for item in inventory[key]:
            if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k] for k in ('source', 'url', 'reason')):
                raise ValueError(f'Each {key} entry requires source, url and reason strings')
            if 'fragment_only' in item and not isinstance(item['fragment_only'], bool):
                raise ValueError('fragment_only must be a boolean')
            if key == 'examples':
                parsed = urlsplit(item['url'])
                if parsed.scheme not in ('http', 'https') or not parsed.hostname:
                    raise ValueError(f'Example URL must be absolute HTTP(S): {item["url"]}')
                parsed.port
    return inventory


def collect(site, site_url, inventory, report):
    if not site.is_dir():
        raise ValueError(f'Site directory does not exist: {site}')
    pages = {}
    for path in sorted(site.rglob('*.html')):
        pages[path.relative_to(site).as_posix()] = Page(path.read_text(encoding='utf-8'))
        report['counts']['pages'] += 1
    if not pages or 'index.html' not in pages:
        raise ValueError('Site must contain HTML pages and a root index.html')
    references = []
    for source, page in pages.items():
        base = urljoin(site_url, source)
        if page.base:
            base = urljoin(base, page.base)
        for attribute, url in page.references:
            references.append({'source': source, 'attribute': attribute, 'url': url,
                               'resolved_url': urljoin(base, url)})
    for path in sorted(site.rglob('*.css')):
        source = path.relative_to(site).as_posix()
        for url in css_urls(path.read_text(encoding='utf-8')):
            references.append({'source': source, 'attribute': 'css', 'url': url,
                               'resolved_url': urljoin(urljoin(site_url, source), url)})
    for path in sorted([*site.glob('llms.txt'), *site.rglob('*.md')]):
        source = path.relative_to(site).as_posix()
        for url in markdown_urls(path.read_text(encoding='utf-8')):
            references.append({'source': source, 'attribute': 'markdown', 'url': url,
                               'resolved_url': urljoin(urljoin(site_url, source), url)})
    for item in inventory['examples']:
        references.append({'source': item['source'], 'attribute': 'example', 'url': item['url'],
                           'resolved_url': item['url']})
    return pages, references


def check_internal(site, site_url, pages, references, inventory, report):
    origin = urlsplit(site_url)
    host = origin.hostname
    hosts = {host, host.removeprefix('www.'), 'www.' + host.removeprefix('www.')}
    exceptions = {(x['source'], x['url']): x for x in inventory['exceptions']}
    external = defaultdict(list)
    destinations = set()
    for reference in references:
        report['counts']['references'] += 1
        parsed = urlsplit(reference['resolved_url'])
        if parsed.scheme not in ('http', 'https'):
            report['counts']['skipped_non_http'] += 1
            continue
        if not parsed.hostname:
            raise ValueError(f'HTTP URL has no hostname: {reference["resolved_url"]}')
        # Accessing port validates malformed ports even for same-site URLs.
        default_port = 80 if parsed.scheme == 'http' else 443
        port = parsed.port if parsed.port is not None else default_port
        custom_port = origin.port is not None and origin.port != (80 if origin.scheme == 'http' else 443)
        site_port = origin.port if custom_port else default_port
        same_site = parsed.hostname in hosts and port == site_port and (not custom_port or parsed.scheme == origin.scheme)
        destinations.add(reference['resolved_url'])
        exception = exceptions.get((reference['source'], reference['url']))
        if exception:
            report['exceptions'].append({**reference, 'reason': exception['reason'],
                                         'fragment_only': exception.get('fragment_only', False)})
            if not exception.get('fragment_only'):
                continue
            if same_site or not parsed.fragment:
                raise ValueError('fragment_only exceptions must name an external URL fragment')
            reference = {**reference, 'fragment_exception': exception['reason']}
        if not same_site:
            external[reference['resolved_url']].append(reference)
            report['counts']['external_references'] += 1
            continue
        report['counts']['internal_references'] += 1
        target = (site / unquote(parsed.path).lstrip('/')).resolve()
        if not target.is_relative_to(site):
            raise ValueError(f'URL escapes the site directory: {reference["resolved_url"]}')
        if target.is_dir():
            target /= 'index.html'
        target_name = target.relative_to(site).as_posix()
        if not target.is_file():
            report['failures'].append({**reference, 'kind': 'missing_file', 'target': target_name})
        else:
            fragment = unquote(parsed.fragment).split(':~:text=', 1)[0]
            if fragment and target_name in pages and fragment not in pages[target_name].anchors:
                report['failures'].append({**reference, 'kind': 'missing_anchor', 'target': target_name + '#' + fragment})
    report['counts']['unique_destinations'] = len(destinations)
    report['counts']['unique_external_destinations'] = len(external)
    return external


class RedirectLimitError(Exception):
    pass


class Redirects(HTTPRedirectHandler):
    max_repeats = 100
    max_redirections = 100

    def __init__(self):
        self.chain = []

    def redirect_request(self, request, response, code, message, headers, new_url):
        self.chain.append({'url': request.full_url, 'status': code, 'destination': new_url,
                           'location': headers.get('Location', headers.get('URI', new_url))})
        if len(self.chain) > 5:
            raise RedirectLimitError('More than five redirects')
        return super().redirect_request(request, response, code, message, headers, new_url)


def fetch(url, timeout, retries):
    """Inspect only the supplied URL; do not crawl links on third-party pages."""
    for attempt in range(retries + 1):
        redirects = Redirects()
        result = {'final_url': url, 'status': None, 'redirects': redirects.chain,
                  'attempts': attempt + 1, 'title': '', '_anchors': None}
        try:
            request = Request(url, headers={'User-Agent': 'Kubescape-docs-linkcheck/1.0',
                                           'Accept': 'text/html,*/*;q=0.8'})
            with build_opener(redirects).open(request, timeout=timeout) as response:
                result.update(status=response.status, final_url=response.url, kind='reachable')
                if response.headers.get_content_type() in ('text/html', 'application/xhtml+xml'):
                    # Bound response memory. Large/dynamic pages require manual fragment review.
                    limit = 2 * 1024 * 1024
                    content = response.read(limit + 1)
                    if len(content) <= limit:
                        page = Page(content.decode(response.headers.get_content_charset() or 'utf-8', errors='replace'),
                                    collect_resources=False)
                        result['_anchors'] = page.anchors
                        result['title'] = ' '.join(page.title.split())
        except HTTPError as error:
            result.update(status=error.code, final_url=error.url,
                          kind={401: 'access_denied', 403: 'access_denied', 429: 'rate_limited',
                                404: 'not_found', 410: 'not_found'}.get(error.code, 'http_error'))
            error.close()
        except RedirectLimitError as error:
            result.update(kind='redirect_limit', detail=str(error))
        except (URLError, OSError) as error:
            reason = getattr(error, 'reason', error)
            result.update(kind='timeout' if isinstance(reason, TimeoutError) else 'network_error', detail=str(reason))
        if attempt == retries or not (result['kind'] in ('timeout', 'network_error', 'rate_limited') or (result['status'] or 0) >= 500):
            return result
        time.sleep(1)


def check_external(external, report, timeout, retries, checkpoint):
    groups = defaultdict(list)
    for url in external:
        groups[urldefrag(url)[0]].append(url)
    report['counts']['external_requests'] = 0
    executor = ThreadPoolExecutor(max_workers=4)
    try:
        futures = {executor.submit(fetch, base, timeout, retries): base for base in groups}
        for future in as_completed(futures):
            base = futures[future]
            response = future.result()
            report['counts']['external_requests'] += 1
            for url in groups[base]:
                result = {key: value for key, value in response.items() if not key.startswith('_')}
                result.update(url=url, references=external[url])
                fragment = urlsplit(url).fragment
                for redirect in result['redirects']:
                    if '#' in redirect['location']:
                        fragment = urlsplit(redirect['location']).fragment
                fragment = unquote(fragment).split(':~:text=', 1)[0]
                result['fragment'] = fragment
                if result['kind'] == 'reachable' and fragment:
                    if response['_anchors'] is None or all(ref.get('fragment_exception') for ref in external[url]):
                        result['kind'] = 'fragment_unverified'
                    elif fragment not in response['_anchors'] and not (
                            urlsplit(result['final_url']).hostname == 'github.com'
                            and 'user-content-' + fragment in response['_anchors']):
                        result['kind'] = 'missing_anchor'
                report['external_results'].append(result)
                if result['kind'] in ('missing_anchor', 'not_found', 'http_error'):
                    report['failures'].append(result)
                elif result['kind'] != 'reachable':
                    report['unverified'].append(result)
            if report['counts']['external_requests'] % 10 == 0:
                checkpoint()
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
    for key in ('external_results', 'failures', 'unverified'):
        report[key].sort(key=lambda item: (item.get('url', ''), item.get('source', '')))


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def write_report(report, path):
    for key in ('failures', 'exceptions', 'unverified', 'errors'):
        report['counts'][key] = len(report[key])
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    report = {'complete': False, 'mode': None, 'started_at': datetime.now(timezone.utc).isoformat(), 'counts': {
        'pages': 0, 'references': 0, 'internal_references': 0,
        'external_references': 0, 'skipped_non_http': 0, 'unique_destinations': 0,
        'unique_external_destinations': 0},
        'failures': [], 'exceptions': [], 'unverified': [], 'errors': [], 'external_results': []}
    report_path = None
    if '--report' in argv and argv.index('--report') + 1 < len(argv):
        report_path = Path(argv[argv.index('--report') + 1])
    else:
        report_path = next((Path(arg.split('=', 1)[1]) for arg in argv if arg.startswith('--report=')), None)
    code = 2
    try:
        parser = ArgumentParser(description=__doc__)
        parser.add_argument('mode', choices=('internal', 'external'))
        parser.add_argument('--site-dir', required=True, type=Path)
        parser.add_argument('--site-url', default='https://kubescape.io/')
        parser.add_argument('--inventory', type=Path, default=DEFAULT_INVENTORY)
        parser.add_argument('--report', required=True, type=Path)
        parser.add_argument('--timeout', type=float, default=15, help='Per-request timeout in seconds (external mode)')
        parser.add_argument('--retries', type=int, default=1, help='Retry transient failures up to twice (external mode)')
        args = parser.parse_args(argv)
        report_path = args.report
        report['mode'] = args.mode
        write_report(report, report_path)
        base = urlsplit(args.site_url)
        if base.scheme not in ('http', 'https') or not base.hostname or base.path not in ('', '/') or base.query or base.fragment:
            raise ValueError('--site-url must be the HTTP(S) site origin, without a path or query')
        base.port
        if not 0 < args.timeout <= 60 or not 0 <= args.retries <= 2:
            raise ValueError('--timeout must be between 0 and 60 seconds; --retries must be 0, 1 or 2')
        site = args.site_dir.resolve()
        inventory = load_inventory(args.inventory)
        pages, references = collect(site, args.site_url.rstrip('/') + '/', inventory, report)
        external = check_internal(site, args.site_url, pages, references, inventory, report)
        if args.mode == 'external':
            write_report(report, report_path)
            check_external(external, report, args.timeout, args.retries, lambda: write_report(report, report_path))
        report['complete'] = True
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        code = 1 if args.mode == 'internal' and report['failures'] else 0
    except (Exception, KeyboardInterrupt) as error:
        report['errors'].append(f'{type(error).__name__}: {error}')
    for key in ('failures', 'exceptions', 'unverified', 'errors'):
        report['counts'][key] = len(report[key])
    if report_path:
        try:
            write_report(report, report_path)
        except OSError as error:
            print(f'Cannot write report: {error}', file=sys.stderr)
            return 2
    counts = report['counts']
    status = 'complete' if report['complete'] else 'INCOMPLETE'
    print(f'**{(report["mode"] or "Link").capitalize()} link check: {status}**')
    print(f'{counts["pages"]} pages; {counts["references"]} references; '
          f'{counts["failures"]} findings; {counts["exceptions"]} exceptions; '
          f'{counts["unverified"]} unverified. Report: `{report_path}`')
    for error in report['errors']:
        print(f'Error: {error}')
    return code


if __name__ == '__main__':
    sys.exit(main())
