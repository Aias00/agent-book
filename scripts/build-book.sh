#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
mkdir -p docs/site docs/site/downloads docs/downloads downloads
chapters=(manuscript/00-preface.md manuscript/01-boundary.md manuscript/02-model-and-interface.md manuscript/03-agent-loop.md manuscript/04-tools.md manuscript/05-context.md manuscript/06-rag.md manuscript/07-memory.md manuscript/08-workflows.md manuscript/09-multi-agent.md manuscript/10-mcp.md manuscript/11-security.md manuscript/12-evaluation.md manuscript/13-observability.md manuscript/14-performance.md manuscript/15-capstone.md manuscript/16-maintenance.md manuscript/99-appendix.md)
pandoc "${chapters[@]}" --metadata-file=metadata.yaml --css=assets/style.css --toc --standalone --epub-cover-image=assets/cover.svg -o /tmp/agent-book.epub
cp /tmp/agent-book.epub downloads/agent-engineering-java.epub
cp downloads/agent-engineering-java.epub docs/downloads/agent-engineering-java.epub
cp downloads/agent-engineering-java.epub docs/site/downloads/agent-engineering-java.epub
python3 scripts/build_site.py
python3 scripts/verify_site.py
