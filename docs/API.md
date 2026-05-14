# 路由設計 (API Design)

為了實現「任務內容編輯與更新」的分組作業需求，我們在此規劃後端路由的設計。

## 1. 路由總覽

| 功能 | HTTP 方法 | URL 路徑 | 對應模板/回傳值 | 說明 |
|---|---|---|---|---|
| 首頁 | GET | `/` | `templates/index.html` | 顯示所有任務，並提供 Inline Edit 測試環境 |
| 更新任務 | PUT | `/api/tasks/<int:id>` | JSON | 接收前端的 JSON 內容，寫入 SQLite，回傳成功與否 |

> **備註**：由於前端使用 Vanilla JavaScript Fetch API，因此我們可以合法地使用 `PUT` 方法來進行非同步更新，不受限於傳統 HTML 表單的 GET/POST。

## 2. 每個路由的詳細說明

### `GET /`
- **輸入**：無
- **處理邏輯**：從資料庫讀取所有任務 (包含已完成、未完成)。
- **輸出**：渲染 `index.html`，並將任務列表注入。
- **錯誤處理**：若資料庫連線失敗，由 Flask 預設處理回傳 500。

### `PUT /api/tasks/<int:id>`
- **輸入**：URL 參數帶有任務 `id`；Request Body 帶有 JSON `{ "title": "新內容" }`。
- **處理邏輯**：
  1. 檢查是否存在 `title` 欄位且不為空。
  2. 根據 `id` 尋找資料庫中的任務，執行 UPDATE 指令。
- **輸出**：回傳 JSON `{"success": true, "title": "新內容"}`。
- **錯誤處理**：
  - 若找不到指定任務或更新失敗，回傳 HTTP 404 與錯誤 JSON。
  - 若 `title` 格式錯誤或為空，回傳 HTTP 400 與錯誤 JSON。

## 3. Jinja2 模板清單

- `templates/index.html`: 單一主畫面，包含任務列表，並負責引入 CSS/JS 檔案以處理您的編輯互動功能。
