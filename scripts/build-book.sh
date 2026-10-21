#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
mkdir -p docs/site docs/site/downloads docs/downloads downloads
chapters=(manuscript/00-preface.md manuscript/01-boundary.md manuscript/02-model-and-interface.md manuscript/03-agent-loop.md manuscript/04-tools.md manuscript/05-context.md manuscript/06-rag.md manuscript/07-memory.md manuscript/08-workflows.md manuscript/09-multi-agent.md manuscript/10-mcp.md manuscript/11-security.md manuscript/12-evaluation.md manuscript/13-observability.md manuscript/14-performance.md manuscript/15-capstone.md manuscript/16-maintenance.md manuscript/99-appendix.md)
pandoc "${chapters[@]}" --metadata-file=metadata.yaml --css=assets/style.css --toc --standalone --epub-cover-image=assets/cover.svg -o /tmp/agent-book.epub
cp /tmp/agent-book.epub downloads/agent-engineering-java.epub
cp downloads/agent-engineering-java.epub docs/downloads/agent-engineering-java.epub
cp downloads/agent-engineering-java.epub docs/site/downloads/agent-engineering-java.epub
for file in "${chapters[@]}"; do base="$(basename "$file" .md)"; pandoc "$file" --metadata-file=metadata.yaml --css=style.css --standalone -o "docs/site/$base.html"; done
python3 - <<'PY'
from pathlib import Path
names=[p.stem for p in sorted(Path('manuscript').glob('*.md'))]
links=''.join(f'<li><a href="{n}.html">{n}</a></li>' for n in names)
Path('docs/site/index.html').write_text(f'''<!doctype html><meta charset="utf-8"><title>Agent 工程入门与实战</title><link rel="stylesheet" href="style.css"><main><h1>Agent 工程入门与实战</h1><p>Java 开发者学习指南：原理、离线示例、失败分析与工程验收。</p><p><a href="downloads/agent-engineering-java.epub">下载 EPUB</a></p><nav class="nav"><h2>目录</h2><ol>{links}</ol></nav></main>''',encoding='utf-8')
PY
cp assets/style.css docs/site/style.css
