#!/usr/bin/env python3
"""Build the chapter reader without regenerating or changing the EPUB."""
from html import escape
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs/site"
TITLE = "Agent 工程入门与实战"
EPUB = "downloads/agent-engineering-java.epub"


def layout(title, content, current="index"):
    navigation = "\n".join(
        f'<li><a href="{stem}.html"' + (' aria-current="page"' if current == stem else '')
        + f'>{escape(name)}</a></li>' for stem, name, _ in chapters
    )
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f7f3">
<meta name="description" content="面向 Java 开发者的 Agent 工程学习书：知识库助手、工具调用、检索、工作流、安全、评测与维护。">
<title>{escape(title)} · {TITLE}</title>
<link rel="stylesheet" href="style.css"><script src="reader.js" defer></script>
</head><body id="top" data-page="{current}">
<a class="skip-link" href="#content">跳到正文</a>
<header class="site-header"><a class="site-brand" href="index.html"><span class="brand-mark" aria-hidden="true">A<span>_</span></span>Agent 工程入门与实战</a>
<nav class="header-links" aria-label="站点导航"><a href="https://aias00.github.io/#books">电子书架</a><a class="header-download" href="{EPUB}" download>下载 EPUB ↓</a></nav>
<div class="reading-progress" aria-hidden="true"><span id="progress-bar"></span></div></header>
<div class="reader-layout"><aside class="sidebar" aria-label="阅读导航">
<details class="chapter-menu" id="chapter-menu" open><summary>全书目录 <span class="chapter-count">16 章 · 前言与附录</span><span class="menu-chevron" aria-hidden="true">⌄</span></summary>
<div class="toc-scroll"><nav id="TOC" aria-label="全书章节"><ul><li><a href="index.html"{' aria-current="page"' if current == 'index' else ''}>阅读指南</a></li>{navigation}</ul></nav></div></details>
<div class="sidebar-footer">JAVA / AGENT ENGINEERING<br><a href="{EPUB}" download>下载 EPUB</a><a href="https://github.com/Aias00/agent-book">GitHub ↗</a></div></aside>
<main id="content" tabindex="-1">{content}</main></div>
</body></html>'''


def tools(label):
    return f'''<div class="reader-tools"><span class="reader-label">{escape(label)}</span>
<div class="enhanced-controls" hidden><div class="font-controls"><button id="font-smaller" type="button" aria-label="缩小正文字号">A−</button><button id="font-larger" type="button" aria-label="放大正文字号">A+</button></div>
<button id="theme-toggle" type="button" aria-label="切换阅读主题">切换深色</button></div></div>'''


def page_link(index, direction):
    if not 0 <= index < len(chapters):
        return ''
    stem, name, _ = chapters[index]
    return f'<a class="{direction}" href="{stem}.html"><span>{"← 上一章" if direction == "prev" else "下一章 →"}</span><strong>{escape(name)}</strong></a>'


chapters = []
for path in sorted((ROOT / "manuscript").glob("*.md")):
    manuscript = path.read_text()
    heading = re.search(r"^#\s+(.+)$", manuscript, re.M)
    if not heading:
        raise ValueError(f"Missing chapter title: {path}")
    chapters.append((path.stem, heading[1], path))
assert len(chapters) == 18
SITE.mkdir(parents=True, exist_ok=True)
(SITE / "assets").mkdir(exist_ok=True)
(SITE / "downloads").mkdir(exist_ok=True)
shutil.copy2(ROOT / "assets/cover.svg", SITE / "assets/cover.svg")
shutil.copy2(ROOT / EPUB, SITE / EPUB)
for source, destination in [("reader.css", "style.css"), ("reader.js", "reader.js")]:
    shutil.copy2(ROOT / "web" / source, SITE / destination)

for index, (stem, title, path) in enumerate(chapters):
    fragment = subprocess.check_output(['pandoc', str(path), '--from=markdown', '--to=html5', '--wrap=none'], text=True)
    fragment = re.sub(r'(<table\b.*?</table>)', r'<div class="table-scroll" role="region" aria-label="可横向滚动的表格" tabindex="0">\1</div>', fragment, flags=re.S)
    page = tools("在线阅读") + f'<div class="chapter-meta"><a href="index.html">阅读指南</a><span>第 {index + 1} / {len(chapters)} 节</span></div>'
    page += f'<article class="book-content">{fragment}</article>'
    page += '<nav class="chapter-pagination" aria-label="章节翻页">' + page_link(index - 1, 'prev') + page_link(index + 1, 'next') + '</nav>'
    (SITE / f"{stem}.html").write_text(layout(title, page, stem))

cards = ''.join(f'<a class="chapter-card" href="{stem}.html"><span>{"前言" if i == 0 else "附录" if i == 17 else f"CHAPTER {i:02}"}</span>{escape(title)}</a>' for i, (stem, title, _) in enumerate(chapters))
intro = f'''<section class="book-intro"><div class="intro-copy"><p class="eyebrow">JAVA / AGENT ENGINEERING</p>
<h1>Agent 工程<br><span>入门与实战</span></h1><p class="intro-description">写给 Java 开发者的学习指南。<br>围绕一个可测试的知识库助手，从原理走向工程实践。</p>
<p class="book-facts"><span>16 章 · 前言与附录</span><span>Java 21</span><span>离线示例 · 练习与答案</span></p>
<div class="intro-actions"><a class="button button-primary" href="{chapters[0][0]}.html">开始阅读 →</a><a class="button button-secondary" href="{EPUB}" download>下载 EPUB ↓</a></div><p class="resume-note" id="resume-note" hidden></p></div>
<div class="cover-preview"><img src="assets/cover.svg" alt="Agent 工程入门与实战电子书封面" width="600" height="900"></div></section>'''
intro += tools("选择章节") + '<h2 class="home-heading">从一个知识库助手开始</h2><div class="chapter-grid">' + cards + '</div>'
(SITE / "index.html").write_text(layout("阅读指南", intro))
(SITE / ".nojekyll").touch()
print(f"Built reading guide and {len(chapters)} chapter pages; EPUB copied unchanged")
