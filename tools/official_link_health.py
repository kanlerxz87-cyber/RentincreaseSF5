#!/usr/bin/env python3
"""Inventory published external hrefs; optionally probe them from a network-enabled host.

This is an availability check, not a legal or factual verification. A network
failure, access denial, HTTP 200 error page, or redirect must be reviewed by a
human. The sandbox may be unable to reach government hosts at all.
"""
from __future__ import annotations

import argparse
import concurrent.futures
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HREF = re.compile(r'''\bhref\s*=\s*(["'])(.*?)\1''', re.I | re.S)


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        # HTMLParser decodes a bare '&sectionNum' as '&sect' + 'ionNum',
        # although browsers do not do that in attributes. Preserve the raw
        # attribute and decode only the escaped ampersands used in URLs.
        match = HREF.search(self.get_starttag_text())
        if match:
            url = match.group(2).replace('&amp;', '&').replace('&#38;', '&').replace('&#x26;', '&')
            if urlsplit(url).scheme in ('http', 'https'):
                self.urls.append(url)


def inventory():
    occurrences = {}
    for directory in (ROOT, ROOT / 'pages', ROOT / 'dashboard'):
        for path in sorted(directory.glob('*.html')):
            parser = Links()
            parser.feed(path.read_text(encoding='utf-8'))
            for url in parser.urls:
                occurrences.setdefault(url, set()).add(str(path.relative_to(ROOT)))
    return occurrences


def probe(url):
    try:
        request = Request(url, headers={'User-Agent': 'SF-rent-research-link-check/1.0'})
        with urlopen(request, timeout=15) as response:
            return f'HTTP {response.status}; final URL {response.geturl()}'
    except HTTPError as exc:
        return f'HTTP {exc.code}; manual review required'
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return f'INCONCLUSIVE ({type(exc).__name__}); manual review required'


def self_test():
    parser = Links()
    parser.feed('<a href="https://example.gov/?lawCode=CIV&sectionNum=827">x</a>'
                '<a href="https://example.gov/?a=1&amp;b=2">x</a>')
    assert parser.urls == ['https://example.gov/?lawCode=CIV&sectionNum=827',
                           'https://example.gov/?a=1&b=2']
    print('PASS: raw query parameters and escaped ampersands')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='probe URLs; requires external network access')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    urls = inventory()
    print(f'{len(urls)} unique external URLs in root, pages/ and dashboard/; mirrors excluded')
    if not args.check:
        for url in sorted(urls):
            print(f'{url}\t{", ".join(sorted(urls[url]))}')
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(probe, sorted(urls)))
    for url, result in zip(sorted(urls), results):
        print(f'{result}\t{url}\t{", ".join(sorted(urls[url]))}')
    print('Review redirects and response content manually; HTTP 200 alone does not verify content.')


if __name__ == '__main__':
    main()
