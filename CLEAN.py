import os
import re

# 設定子路徑名稱
repo_name = 'knowledgesharehub'

def optimize_static_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 解決黑色區塊問題：將 data-src 還原為 src，並移除 smush 相關類別
    # 這是處理您圖中「黑色長條物」的核心邏輯
    content = re.sub(r'data-src="([^"]+)"', r'src="\1"', content)
    content = re.sub(r'class="[^"]*lazyload[^"]*"', '', content)
    content = re.sub(r'style="--smush-placeholder[^"]*"', '', content)

    # 2. 清理無用 JS 連結（留言、表單、懶加載補丁）
    useless_scripts = [
        r'<script[^>]*src="[^"]*smush-lazy-load[^"]*"></script>',
        r'<script[^>]*src="[^"]*comment-reply[^"]*"></script>',
        r'<script[^>]*src="[^"]*contact-form-7[^"]*"></script>',
        r'<section[^>]*id="comments"[^>]*>.*?</section>', # 移除整個留言區塊
        r'<div[^>]*class="comment-respond"[^>]*>.*?</div>'
    ]
    for pattern in useless_scripts:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # 3. 修正導覽欄樣式路徑：確保所有連結都包含子目錄
    # 避免導覽欄 CSS 跑掉
    content = content.replace('src="/wp-content/', f'src="/{repo_name}/wp-content/')
    content = content.replace('href="/wp-content/', f'href="/{repo_name}/wp-content/')
    content = content.replace('href="/wp-includes/', f'href="/{repo_name}/wp-includes/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 執行處理
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            optimize_static_html(os.path.join(root, file))

print("優化完成！黑色佔位符與無用連結已清理。")