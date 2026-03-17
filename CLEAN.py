import os
import re

repo_name = 'knowledgesharehub'

def fix_redis_page_issue(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 強制將 Smush 的佔位符替換回原始圖片路徑
    content = re.sub(r'src="data:image/svg\+xml;base64,[^"]+"', '', content) # 移除透明占位圖
    content = re.sub(r'data-src="([^"]+)"', r'src="\1"', content)
    
    # 2. 強制移除導致黑色長條的 Smush CSS 類別與變數
    content = re.sub(r'class="[^"]*lazyload[^"]*"', 'class="fixed-image"', content)
    content = re.sub(r'style="[^"]*--smush-placeholder[^"]*"', '', content)
    content = re.sub(r'opacity:\s*0;', 'opacity: 1;', content)

    # 3. 處理 Elementor 嵌套元件在子目錄下的路徑
    content = content.replace('src="/wp-content/', f'src="/{repo_name}/wp-content/')
    content = content.replace('href="/wp-content/', f'href="/{repo_name}/wp-content/')
    content = content.replace('data-srcset="/wp-content/', f'data-srcset="/{repo_name}/wp-content/')
    
    # 4. 移除失效的 Smush 懶加載 JS，避免它干擾頁面渲染
    content = re.sub(r'<script[^>]*smush-lazy-load\.min\.js[^>]*></script>', '', content)

    # 5. 移除自動產生且在編輯器中造成 JS 語法錯誤的 emoji loader module 區塊
    #    （不影響文章主體與版面，只影響 emoji 支援偵測腳本）
    content = re.sub(
        r'<script type="module">\s*/\*! This file is auto-generated \*/.*?wp-emoji-loader\.min\.js[^<]*</script>\s*',
        '',
        content,
        flags=re.DOTALL,
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 遍歷目錄處理所有 HTML
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            fix_redis_page_issue(os.path.join(root, file))

print("黑色區塊修復完成！")