# API 路由設計 (API Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :---: | :--- | :--- | :--- |
| **任務列表** | `GET` | `/` 或 `/tasks` | `templates/index.html` | 顯示首頁，包含所有待辦與已完成任務，以及新增任務的表單。 |
| **新增任務** | `POST` | `/tasks/create` | — | 接收表單資料，寫入資料庫後重導向回 `/`。 |
| **切換狀態** | `POST` | `/tasks/<int:id>/toggle` | — | 將指定任務的狀態反轉 (完成/待辦)，成功後重導向回 `/`。 |
| **刪除任務** | `POST` | `/tasks/<int:id>/delete` | — | 將指定任務從資料庫刪除，成功後重導向回 `/`。 |

*(註：為了保持操作簡單，本專案將新增與列表畫面整合在同一個頁面 (index.html)，故不另外提供 GET `/tasks/new` 的獨立頁面)*

## 2. 每個路由的詳細說明

### `GET /` (任務列表)
- **輸入**: 無
- **處理邏輯**: 呼叫 `TaskModel.get_all_tasks()`，從資料庫取出所有的任務清單。
- **輸出**: 渲染 `index.html`，並將任務資料傳遞給 Jinja2 模板。
- **錯誤處理**: 若資料庫錯誤，顯示系統錯誤的 flash 訊息。

### `POST /tasks/create` (新增任務)
- **輸入**: HTML 表單提交 (Content-Type: `application/x-www-form-urlencoded`)，欄位包含 `title`。
- **處理邏輯**: 
  1. 驗證 `title` 是否為空字串，若為空則閃示 (flash) 錯誤訊息。
  2. 呼叫 `TaskModel.create_task(title)` 寫入資料庫。
- **輸出**: HTTP 302 重導向回 `/`。
- **錯誤處理**: 若輸入無效或寫入失敗，使用 `flash` 顯示錯誤，並重導向回 `/`。

### `POST /tasks/<int:id>/toggle` (切換狀態)
- **輸入**: URL 路徑參數 `id` (整數)。由點擊勾選框或表單觸發。
- **處理邏輯**: 
  1. 呼叫 `TaskModel.toggle_task_status(id)` 來反轉目前狀態。
- **輸出**: HTTP 302 重導向回 `/`。
- **錯誤處理**: 若 `id` 不存在，回應 404，或 `flash` 錯誤訊息後重導向。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**: URL 路徑參數 `id` (整數)。
- **處理邏輯**: 
  1. 呼叫 `TaskModel.delete_task(id)` 將記錄刪除。
- **輸出**: HTTP 302 重導向回 `/`。

## 3. Jinja2 模板清單

- **`base.html`**: 基礎版型，包含 HTML `<head>` (引用 Bootstrap 5 CDN)、導覽列 (Navbar)、Flash 訊息顯示區塊，以及 `{% block content %}{% endblock %}` 提供子頁面填入。
- **`index.html`**: 首頁內容。繼承 `base.html`。
  - 頂部：新增任務的 `title` 欄位與 Submit 按鈕。
  - 下方：用 `{% for task in tasks %}` 顯示任務列表。
  - 每筆任務需包含：狀態切換的 Checkbox (包在 POST 表單內) 以及刪除按鈕 (包在 POST 表單內)。

## 4. 路由骨架程式碼規劃
檔案建立於 `app/routes/task_routes.py`。
使用 Flask 的 `Blueprint` 來組織路由，方便註冊到 `app.py` 中。
