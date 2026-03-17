import os
import re
from datetime import datetime

try:
    import markdown  # type: ignore
except ImportError:
    markdown = None


RE_BUTTON = re.compile(
    r'\[button\s+text="(?P<text>[^"]+)"\s+url="(?P<url>[^"]+)"\s*\]'
)

RE_ACCORDION = re.compile(
    r'\[accordion\s+title="(?P<title>[^"]+)"\](?P<body>.*?)\[/accordion\]',
    re.DOTALL,
)


def ensure_markdown():
    if markdown is None:
        raise RuntimeError(
            "需要安裝 python-markdown 套件：pip install markdown"
        )


def repo_name_from_cwd() -> str:
    return os.path.basename(os.getcwd())


def render_button(text: str, url: str) -> str:
    return (
        f'<div class="elementor-widget elementor-widget-button">'
        f'<div class="elementor-widget-container">'
        f'<div class="elementor-button-wrapper">'
        f'<a href="{url}" class="elementor-button-link elementor-button elementor-size-sm" role="button">'
        f'<span class="elementor-button-content-wrapper">'
        f'<span class="elementor-button-text">{text}</span>'
        f'</span></a></div></div></div>'
    )


def render_accordion(title: str, inner_markdown: str) -> str:
    """
    產生類 Elementor Accordion 的 HTML 結構。
    內文先轉成 HTML 再嵌入。
    """
    ensure_markdown()
    inner_html = markdown.markdown(inner_markdown.strip())

    return (
        '<div class="elementor-widget elementor-widget-accordion">'
        '<div class="elementor-widget-container">'
        '<div class="elementor-accordion" role="tablist">'
        '<div class="elementor-accordion-item">'
        '<div class="elementor-accordion-title" role="button" tabindex="0" aria-expanded="false">'
        '<span class="elementor-accordion-icon elementor-accordion-icon-right">'
        '<span class="elementor-accordion-icon-closed"><i class="eicon-plus" aria-hidden="true"></i></span>'
        '<span class="elementor-accordion-icon-opened"><i class="eicon-minus" aria-hidden="true"></i></span>'
        '</span>'
        f'<span class="elementor-accordion-title-text">{title}</span>'
        '</div>'
        '<div class="elementor-accordion-content" aria-hidden="true">'
        f'{inner_html}'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )


def apply_shortcodes(text: str) -> str:
    """
    將 Markdown 內的短代碼轉換成對應 HTML。
    先處理 accordion（區塊），再處理 button（單一行）。
    """

    def accordion_repl(match: re.Match) -> str:
        title = match.group("title")
        body = match.group("body")
        return render_accordion(title, body)

    text = RE_ACCORDION.sub(accordion_repl, text)

    def button_repl(match: re.Match) -> str:
        return render_button(match.group("text"), match.group("url"))

    text = RE_BUTTON.sub(button_repl, text)

    return text


def markdown_to_html(md_text: str) -> str:
    ensure_markdown()
    # 先展開短代碼，再讓 markdown 負責一般排版
    md_with_shortcodes = apply_shortcodes(md_text)
    return markdown.markdown(md_with_shortcodes, extensions=["extra"])


def build_html_page(template: str, title: str, content_html: str, date_str: str) -> str:
    html = template.replace("{{TITLE}}", title)
    html = html.replace("{{CONTENT}}", content_html)
    html = html.replace("{{DATE}}", date_str)

    # --- 路徑與懶加載清理 ---
    # 1. 確保圖片使用子目錄路徑
    html = html.replace('src="/wp-content/', f'src="/{REPO_NAME}/wp-content/')
    html = html.replace('href="/wp-content/', f'href="/{REPO_NAME}/wp-content/')
    
    # 2. 清理 Smush 導致的黑色區塊
    # 將 Markdown 生成的 <img> 強制轉為不帶 Smush 佔位符的格式
    html = re.sub(r'class="[^"]*lazyload[^"]*"', '', html)
    html = re.sub(r'style="[^"]*--smush-placeholder[^"]*"', '', html)
    
    return html


def extract_title(md_text: str, fallback_slug: str) -> str:
    """
    優先使用第一行的 Markdown H1 作為標題，沒有就用檔名 slug。
    """
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        if stripped:
            break
    return fallback_slug


def process_markdown_file(md_path: str, template: str, output_dir: str) -> None:
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    slug = os.path.splitext(os.path.basename(md_path))[0]
    title = extract_title(md_text, slug)

    # 日期使用檔案最後修改時間，格式比照站內：DD/MM/YYYY
    mtime = datetime.fromtimestamp(os.path.getmtime(md_path))
    date_str = mtime.strftime("%d/%m/%Y")

    content_html = markdown_to_html(md_text)
    final_html = build_html_page(template, title, content_html, date_str)

    # 輸出到 output_dir/slug/index.html
    target_dir = os.path.join(output_dir, slug)
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, "index.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Generated: {out_path}")


def main():
    ensure_markdown()

    root = os.getcwd()
    template_path = os.path.join(root, "post_template.html")
    posts_dir = os.path.join(root, "my_posts")
    output_dir = os.path.join(root, "generated_posts")

    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"找不到模板檔案: {template_path}")

    if not os.path.isdir(posts_dir):
        raise FileNotFoundError(f"找不到 Markdown 目錄: {posts_dir}")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    for name in os.listdir(posts_dir):
        if not name.lower().endswith(".md"):
            continue
        md_path = os.path.join(posts_dir, name)
        process_markdown_file(md_path, template, output_dir)


if __name__ == "__main__":
    main()

