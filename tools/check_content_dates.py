#!/usr/bin/env python3
"""Regression checks for editorial dates versus rate verification (stdlib only)."""
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import content_dates as D
from markets import VERIFIED


class Dates(HTMLParser):
    def __init__(self):
        super().__init__()
        self.times = []
        self.schemas = []
        self.in_schema = False
        self.buf = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'time':
            self.times.append(attrs.get('datetime'))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema = True
            self.buf = ''

    def handle_data(self, data):
        if self.in_schema:
            self.buf += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schemas.append(json.loads(self.buf))
            self.in_schema = False


def main():
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    entries = ET.parse(ROOT / 'sitemap.xml').getroot().findall('s:url', ns)
    schema_count = 0
    paths = set()
    for entry in entries:
        path = entry.findtext('s:loc', namespaces=ns).split('.app/')[1]
        paths.add(path)
        expected = D.modified(path)
        assert expected, f'Missing reviewed content date: {path}'
        assert date.fromisoformat(expected) <= date.today(), path
        assert re.fullmatch(r'[a-f0-9]{40}', D.RECORDS[path]['source_commit']), path
        assert entry.findtext('s:lastmod', namespaces=ns) == expected, path
        parsed = Dates()
        parsed.feed((ROOT / path / 'index.html').read_text(encoding='utf-8'))
        for schema in parsed.schemas:
            if schema.get('@type') in ('Article', 'WebApplication'):
                assert schema.get('dateModified') == expected, path
                assert expected in parsed.times, f'No visible update date: {path}'
                assert VERIFIED in parsed.times, f'Lost source verification date: {path}'
                if schema.get('@type') == 'Article':
                    assert 'datePublished' not in schema, f'Unsupported publication date: {path}'
                schema_count += 1
    assert paths == set(D.RECORDS), 'Date registry must match established canonical URLs'
    assert VERIFIED == '2026-10-26', 'This change must not reverify rates'
    assert D.modified('zh/tiktok-shop/malaysia/') == '2026-11-14'
    assert D.modified('zh/shopee/malaysia/') == '2026-11-14'
    assert D.modified('zh/') == '2026-11-14'
    assert D.modified('en/tiktok-shop/malaysia/') != '2026-11-14'
    assert D.modified('zh/guides/tiktok-shop-malaysia-commission-changes-october-2026/') != '2026-11-14'
    assert D.modified('unknown/') is None
    assert D.time_html('unknown/', 'en') == ''
    for lang in ('en', 'zh', 'ru', 'ms'):
        assert D.label(lang) in D.time_html(f'{lang}/', lang)
    counts = Counter(D.modified(path) for path in paths)
    assert len(counts) > 1, 'Do not replace all historical dates with one build date'
    print(f'PASS: {len(paths)} sitemap dates, {schema_count} schema/visible dates; verification retained at {VERIFIED}')
    print('Historical modification dates:', dict(sorted(counts.items())))


if __name__ == '__main__':
    main()
