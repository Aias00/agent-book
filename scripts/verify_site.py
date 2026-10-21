#!/usr/bin/env python3
"""Check chapter coverage, readable navigation and local links in the reader."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs/site"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.headings = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.headings += 1
        for attr in ['href', 'src']:
            if attr in attrs:
                self.links.append(attrs[attr])


pages = {path: Page(path.read_text()) for path in SITE.glob('*.html')}
assert len(pages) == 19, f'Expected guide and 18 chapter pages, got {len(pages)}'
checked = 0
for path, page in pages.items():
    assert page.headings == 1, f'{path.name}: duplicate or missing title'
    assert len(page.ids) == len(set(page.ids)), f'{path.name}: duplicate IDs'
    text = path.read_text()
    assert 'id="chapter-menu"' in text
    assert ('class="chapter-grid"' if path.name == 'index.html' else 'class="book-content"') in text
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.exists(), f'{path.name}: broken link {link}'
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, f'{path.name}: broken anchor {link}'
        checked += 1
for manuscript in (ROOT / 'manuscript').glob('*.md'):
    title = re.search(r'^#\s+(.+)$', manuscript.read_text(), re.M)[1]
    page = SITE / (manuscript.stem + '.html')
    assert title in page.read_text(), f'Missing chapter title: {title}'
original = ROOT / 'downloads/agent-engineering-java.epub'
published = SITE / 'downloads/agent-engineering-java.epub'
assert original.read_bytes() == published.read_bytes(), 'EPUB download changed'
print(f'PASS: {len(pages)} pages, {checked} local links/resources, one title per page, chapter coverage; EPUB SHA256 {hashlib.sha256(published.read_bytes()).hexdigest()}')
