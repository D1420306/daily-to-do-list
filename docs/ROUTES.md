# API 路由與頁面設計 - 每日代辦事項 (Daily To-Do List)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 / 回傳 | 說明 |
| --- | --- | --- | --- | --- |
| 任務列表 | GET | `/` | `index.html` | 讀取資料庫所有任務並在首頁顯示 |
| 新增任務 | POST | `/add` | 重導向 `/` | 接收表單文字 `title`，新增至資料庫後回到首頁 |

## 2. 每個路由的詳細說明

### `GET /` (任務列表)
- **輸入**：無
- **處理邏輯**：呼叫 `database.get_all_tasks()` 取得列表。
- **輸出**：渲染 `index.html` 並將 `tasks` 變數傳入。

### `POST /add` (新增任務)
- **輸入**：HTML 表單中的 `title` 欄位。
- **處理邏輯**：
  - 檢查 `title` 是否為空。若空則可設定 flash message 或直接忽略。
  - 呼叫 `database.add_task(title)`。
- **輸出**：重導向至 `GET /`。

## 3. Jinja2 模板清單

將在 `templates/` 資料夾中建立以下檔案：

1. `base.html`
   - **用途**：定義所有頁面的基本 HTML 結構 (如 `<!DOCTYPE html>`, `<head>`, Navbar, 引入 CSS 等)。
   - **區塊**：定義 `{% block content %}` 讓其他頁面填入內容。
2. `index.html`
   - **用途**：首頁，繼承自 `base.html`。
   - **功能**：
     - 顯示新增任務的表單。
     - 顯示代辦事項的列表（使用 `{% for task in tasks %}`）。
