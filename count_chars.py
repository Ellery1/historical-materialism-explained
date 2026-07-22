import re
import os

BASE_DIR = r"e:\python\historical-materialism-explained"

FILES = [
    "00-前言.md",
    "01-思想溯源与理论形成.md",
    "02-核心原理上-社会存在与社会意识.md",
    "03-核心原理下-社会发展规律与动力.md",
    "04-历史主体论.md",
    "05-社会形态更替理论.md",
    "06-实践验证与历史检验.md",
    "07-常见误解与澄清.md",
    "08-当代价值与现实意义.md",
    "结语.md",
]


def clean_content(text: str) -> str:
    """清理 markdown 内容，移除参考文献、语法符号等，只保留正文。"""

    # 1. 移除参考文献块：从每个 "## 参考文献" 到下一个 "---" 分隔线（含）
    #    处理正文中嵌入的多个参考文献块
    text = re.sub(r'\n## 参考文献\n[\s\S]*?\n---\n', '\n', text)
    #    处理文件末尾的参考文献块（无后续 ---）
    text = re.sub(r'\n## 参考文献\n[\s\S]*$', '', text)

    # 2. 移除 --- 分隔线（残留的、非参考文献后的）
    text = re.sub(r'\n---\n', '\n', text)

    # 3. 移除行内脚注引用 [^数字] 或 [^数字,数字]
    text = re.sub(r'\[\^\d+(?:,\d+)*\]', '', text)

    # 4. 移除 markdown 链接 [text](url)
    text = re.sub(r'\[([^\]]*?)\]\([^\)]*?\)', r'\1', text)

    # 5. 移除表格分隔线（如 |------|------|）
    text = re.sub(r'\|[-\s|:]+\|', '', text)

    # 6. 移除 markdown 语法字符
    for ch in ['#', '*', '_', '|', '>', '`', '~', '-']:
        text = text.replace(ch, '')

    # 7. 移除残留的方括号和圆括号（链接语法已处理，这些是残留）
    text = text.replace('[', '').replace(']', '').replace('(', '').replace(')', '')

    # 8. 压缩多余空白行
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def count_chinese_chars(text: str) -> int:
    """统计中文字符数量（含汉字和中文标点）。"""
    pattern = (
        r'[\u4e00-\u9fff'           # CJK 基本汉字
        r'\u3400-\u4dbf'            # CJK 扩展A区
        r'\u3001-\u303f'            # CJK 标点符号（排除 \u3000 表意空格）
        r'\uff01-\uff0f'            # 全角 ! 到 /
        r'\uff1a-\uff20'            # 全角 : 到 @
        r'\uff3b-\uff40'            # 全角 [ 到 `
        r'\uff5b-\uff5e]'           # 全角 { 到 ~
    )
    return len(re.findall(pattern, text))


def main():
    total = 0
    results = []

    for fname in FILES:
        fpath = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fpath):
            print(f"[警告] 文件不存在: {fpath}")
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()

        cleaned = clean_content(raw)
        count = count_chinese_chars(cleaned)
        total += count
        results.append((fname, count))

    # 输出结果
    print("=" * 65)
    print(f"{'章节文件':<42}{'含标点中文字符数':>12}")
    print("=" * 65)
    for fname, count in results:
        print(f"{fname:<40}{count:>12,}")
    print("=" * 65)
    print(f"{'合计':<40}{total:>12,}")
    print("=" * 65)


if __name__ == "__main__":
    main()
