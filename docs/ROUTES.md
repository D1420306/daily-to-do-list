# API 路由與頁面設計 - 每日代辦事項 (Daily To-Do List)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 / 回傳 | 說明 |
| --- | --- | --- | --- | --- |
| 任務列表 | GET | `/` | `index.html` | 讀取資料庫所有任務並在首頁顯示 |
| 新增任務 | POST | `/add` | 重導向 `/` | 接收表單文字 `title`，新增至資料庫後回到首頁 |
| 切換完成 | POST | `/toggle/<int:task_id>` | 重導向 `/` | 根據 ID 找到任務，切換狀態後回到首頁 |
| 刪除任務 | POST | `/delete/<int:task_id>` | 重導向 `/` | 根據 ID 刪除任務，刪除後回到首頁 |
| 編輯任務 | POST | `/edit/<int:task_id>` | 重導向 `/` | 接收表單文字 `new_title`，更新任務後回到首頁 |

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

### `POST /toggle/<int:task_id>` (切換狀態)
- **輸入**：URL 路徑中的 `task_id`。
- **處理邏輯**：呼叫 `database.toggle_task_status(task_id)`。
- **輸出**：重導向至 `GET /`。

### `POST /delete/<int:task_id>` (刪除任務)
- **輸入**：URL 路徑中的 `task_id`。
- **處理邏輯**：呼叫 `database.delete_task(task_id)`。
- **輸出**：重導向至 `GET /`。

### `POST /edit/<int:task_id>` (編輯任務)
- **輸入**：URL 路徑中的 `task_id` 以及 HTML 表單中的 `new_title` 欄位。
- **處理邏輯**：呼叫 `database.update_task_title(task_id, new_title)`。
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
     - 每一筆事項帶有完成/未完成的打勾按鈕、編輯按鈕與刪除按鈕。

## 4. 路由骨架程式碼
已在 `app.py` 中建立包含 Docstring 的路由函式骨架。
