# Markdown → 靜態 HTML 產生器：使用方法報告

## 準備

- **Python**：建議 3.10+（3.8+ 通常也可）
- **套件**：`python-markdown`

安裝方式（在專案根目錄執行）：

```bash
pip install markdown
```

## 資料夾與檔案約定

- **輸入（你寫的文章）**：`my_posts/*.md`
- **模板**：`post_template.html`
- **輸出（產生的靜態頁）**：`generated_posts/<slug>/index.html`

其中 `<slug>` 來自 Markdown 檔名（例如 `my_posts/hello-world.md` → `generated_posts/hello-world/index.html`）。

## 快速開始（最短流程）

1. 在 `my_posts/` 新增一個 Markdown，例如 `my_posts/hello-world.md`
2. 執行：

```bash
python new_post.py
```

3. 生成檔會出現在 `generated_posts/hello-world/index.html`

## Markdown 寫作規範（標題/日期）

- **標題 `{{TITLE}}`**
  - 會優先使用 Markdown 中第一個標題行（例如 `# 我的文章標題`）
  - 若找不到標題行，則改用檔名當標題（例如 `hello-world`）
- **日期 `{{DATE}}`**
  - 目前使用 Markdown 檔案的「最後修改時間」
  - 格式為 `DD/MM/YYYY`（例：`23/09/2025`）

## 短代碼（Shortcode）功能

### 1) 按鈕

[button text="聯絡我們" url="https://example.com/contact"]


會被轉成帶有 `elementor-button` 類別的 HTML，讓 Elementor 的前端 CSS 直接套用按鈕外觀。

### 2) Accordion（摺疊）

語法：

[accordion title="常見問題"]

- 條列
- 連結
- 文字格式
[/accordion]
```

`[accordion]...[/accordion]` 內部的文字會先轉成 HTML，再嵌入 Accordion 結構中。

## 圖片路徑自動修正

腳本會將以下路徑：

- `src="/wp-content/..."`

自動替換成：

- `src="/{repo_name}/wp-content/..."`

其中 `{repo_name}` 會依據「執行 `new_post.py` 時的工作目錄名稱」自動判斷（例如你目前 repo 目錄名是 `knowledgesharehub`，就會變成 `/knowledgesharehub/wp-content/...`）。

## 常見問題（FAQ）

### Q1：我沒看到 `my_posts/`，是要自己新增嗎？

是的，**`my_posts/` 是輸入資料夾**，用來放你的 Markdown 文章。這次我已經把 `my_posts/` 目錄加進 repo（用 `.gitkeep` 讓 Git 追蹤），你只要把 `.md` 放進去即可。

### Q2：我想輸出直接覆蓋到網站根目錄（例如 `/<slug>/index.html`）可以嗎？

可以，之後只要把 `new_post.py` 裡的 `output_dir` 從 `generated_posts/` 改成專案根目錄即可（目前先保守輸出到 `generated_posts/`，避免覆蓋既有頁面）。

### Q3：為什麼我產生的頁面看不到完整導覽列（nav）？

目前 `post_template.html` 內的 `nav.main-navigation` 是「保留結構但未完整貼上所有選單項目」。如果你要求 100% 完全一致（包含所有 menu item），建議我下一步直接從你現有的某篇單文 `index.html` 複製整段 `<nav ...>...</nav>` 到模板中。


文章範例
# 這是我的新文章標題

[button text="我的個人 Github" url="https://github.com/jimmy77733"]

[accordion title="點擊展開查看隱藏內容"]
這是在 Elementor 樣式下的摺疊選單內容，腳本會自動幫你包裝。
[/accordion]

![我的測試圖片](/wp-content/uploads/2026/03/test.jpg)