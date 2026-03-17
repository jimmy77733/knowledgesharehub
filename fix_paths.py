import os
import re

# === 設定區 ===
# 如果您的 GitHub 網址是 jimmy77733.github.io/knowledgesharehub/
# 那麼 repo_name 就是 'knowledgesharehub'
repo_name = 'knowledgesharehub'

# 定義要檢查的檔案路徑（預設為當前目錄）
base_dir = '.' 

# 定義替換規則：搜尋開頭為 "/" 的路徑，並加上子目錄名稱
# 這會處理圖片(src)、樣式表(href)、內文連結(href)等
replacements = [
    (r'src="/wp-content/', f'src="/{repo_name}/wp-content/'),
    (r'href="/wp-content/', f'href="/{repo_name}/wp-content/'),
    (r'src="/wp-includes/', f'src="/{repo_name}/wp-includes/'),
    (r'href="/wp-includes/', f'href="/{repo_name}/wp-includes/'),
    (r'data-src="/wp-content/', f'data-src="/{repo_name}/wp-content/'), # 處理 Lazyload 圖片
    (r'href="/(?![h|#|m|t])', f'href="/{repo_name}/'), # 處理內部文章連結，排除 http, #, mailto, tel
]

def process_files():
    processed_count = 0
    print(f"開始處理路徑修復，目標子目錄: /{repo_name}/ ...")

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = content
                    for pattern, replacement in replacements:
                        new_content = re.sub(pattern, replacement, new_content)

                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        processed_count += 1
                        if processed_count % 100 == 0:
                            print(f"進度：已修正 {processed_count} 個檔案...")
                
                except Exception as e:
                    print(f"無法處理檔案 {file_path}: {e}")

    print(f"--- 處理完成 ---")
    print(f"共計掃描了數千個檔案，成功修正了 {processed_count} 個 HTML 檔案的路徑。")
    print("現在您可以將這些變更 Push 到 GitHub 了！")

if __name__ == "__main__":
    process_files()