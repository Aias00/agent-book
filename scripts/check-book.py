#!/usr/bin/env python3
from pathlib import Path
import re,sys,zipfile
root=Path(__file__).resolve().parents[1]
files=sorted((root/'manuscript').glob('*.md'))
required=['## 学习目标','## 原理','## Java 示例','## 失败分析','## 练习','## 参考答案','## 小结','## 参考资料']
errors=[]; total=0
if len(files)!=18: errors.append(f'expected 18 chapters, found {len(files)}')
for p in files:
    s=p.read_text(encoding='utf-8'); total+=len(re.sub(r'```.*?```','',s,flags=re.S))
    for h in required:
        if h not in s: errors.append(f'{p.name}: missing {h}')
    if '实际运行输出' not in s or '示意输出' not in s: errors.append(f'{p.name}: output labels missing')
if not 40000<=total<=60000: errors.append(f'body characters {total} outside 40000-60000')
epub=root/'downloads/agent-engineering-java.epub'
if epub.exists():
    with zipfile.ZipFile(epub) as z:
        if z.read('mimetype')!=b'application/epub+zip': errors.append('invalid mimetype')
        if 'META-INF/container.xml' not in z.namelist(): errors.append('EPUB missing container')
else: errors.append('EPUB not built yet')
print(f'chapters={len(files)} body_characters={total} epub={epub.exists()}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('book checks passed')
