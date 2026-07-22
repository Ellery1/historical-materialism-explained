import re
import sys

# 从 build_book.py 获取输出文件名，或使用默认名
filename = '用数据解释历史规律-唯物史观简述.html'

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 删除 TOC 中 ch10 相关的整个块
content = re.sub(
    r'<li class="toc-part">参考文献</li>\s*<li class="toc-chapter" data-anchor="ch10-h0">.*?</li>\s*</li>',
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'<li class="toc-part">参考文献</li>\s*<li class="toc-chapter" data-anchor="ch10-h0">.*?</li>',
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(r'<li class="toc-section" data-anchor="ch10-h\d+">.*?</li>', '', content)
content = re.sub(r'<ul class="toc-sections"></ul>\s*', '', content)

# 2. 删除正文中的参考文献章节
content = re.sub(
    r'<div class="part-divider"><span>参考文献</span></div>\s*\n\s*<section class="chapter-card" id="ch10-card">.*?</section>',
    '',
    content,
    flags=re.DOTALL
)

# 3. 删除 JS allAnchors 数组中的 ch10 条目
content = re.sub(r', "ch10-h\d+"', '', content)

# 4. 清理多余空行
content = re.sub(r'\n{3,}', '\n\n', content)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

remaining = len(re.findall('ch10', content))
print(f'Remaining ch10 references: {remaining}')
