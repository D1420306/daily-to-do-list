# FLOWCHART: 每日代辦 (Daily To-Do List) 流程圖設計

本文檔透過視覺化圖表說明「每日代辦」系統中，使用者的操作路徑（User Flow）與系統內部的資料流動（Sequence Diagram）。

## 1. 使用者流程圖（User Flow）

描述使用者進入網頁後，進行各項代辦任務操作的路徑。本專案採單頁面設計模式，所有主要操作皆在首頁完成。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 任務列表]
    
    Home --> Action{要執行什麼操作？}
    
    Action -->|新增任務| Add[在輸入框填寫任務名稱並送出]
    Add --> Home
    
    Action -->|切換狀態| Toggle[勾選 / 取消勾選 任務完成框]
    Toggle --> Home
    
    Action -->|刪除單一任務| Delete[點擊個別任務旁的刪除按鈕]
    Delete --> Home
    
    Action -->|一鍵清理已完成| Clear[點擊『清理已完成』按鈕]
    Clear --> Home
    
    Action -->|編輯任務| Edit[點擊任務文字進入編輯模式 / 送出修改]
    Edit --> Home
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖以「**新增任務**」與「**切換任務狀態**」為例，展示前端瀏覽器、Flask 路由、資料庫模型與 SQLite 之間的互動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite 資料庫

    %% 新增任務流程
    rect rgb(240, 248, 255)
    Note over User, DB: 【流程一】新增任務
    User->>Browser: 在輸入框填寫任務並按下 Enter/新增
    Browser->>Flask: POST /add (帶有任務名稱)
    Flask->>Model: 建立 Task 物件 (title=...)
    Model->>DB: INSERT INTO task (title) VALUES (...)
    DB-->>Model: 回傳成功 (產生 id)
    Model-->>Flask: 物件儲存成功
    Flask-->>Browser: HTTP 302 Redirect 重新導向至首頁 (/)
    Browser->>Flask: GET /
    Flask->>Model: 查詢所有任務
    Model->>DB: SELECT * FROM task
    DB-->>Model: 回傳任務列表資料
    Model-->>Flask: 任務列表物件
    Flask-->>Browser: 渲染 index.html (包含新任務) 並回傳
    Browser-->>User: 畫面顯示新任務
    end

    %% 切換狀態流程
    rect rgb(255, 250, 240)
    Note over User, DB: 【流程二】切換任務狀態 (完成/未完成)
    User->>Browser: 點擊任務的 Checkbox
    Browser->>Flask: POST /toggle/<id>
    Flask->>Model: 查詢該 Task 物件
    Model->>DB: SELECT * FROM task WHERE id = ?
    DB-->>Model: 回傳該任務資料
    Flask->>Model: 改變 is_completed 狀態
    Model->>DB: UPDATE task SET is_completed = ? WHERE id = ?
    DB-->>Model: 更新成功
    Model-->>Flask: 儲存成功
    Flask-->>Browser: HTTP 302 Redirect 重新導向至首頁 (/)
    Browser->>Flask: GET / (重新取得列表並渲染)
    Flask-->>Browser: 回傳更新後的 index.html
    end
```

## 3. 功能清單對照表

本表列出系統所有的主要功能與其對應的 URL 路徑、HTTP 方法及功能描述。

| 功能 | URL 路徑 | HTTP 方法 | 功能描述 |
| --- | --- | --- | --- |
| 瀏覽首頁 | `/` | GET | 顯示所有任務的列表（包含已完成與未完成區塊）。 |
| 新增任務 | `/add` | POST | 接收表單提交的任務名稱，新增到資料庫中。 |
| 切換狀態 | `/toggle/<int:task_id>` | POST | 將指定的任務狀態在「完成」與「未完成」間切換。 |
| 刪除單一任務 | `/delete/<int:task_id>` | POST | 從資料庫中刪除指定的任務。 |
| 編輯任務 | `/edit/<int:task_id>` | POST | 更新指定任務的文字內容。 |
| 一鍵清理已完成 | `/clear-completed` | POST | 將資料庫中所有標記為「已完成」的任務刪除。 |

> **設計備註**：為了確保資料修改的安全性與符合 HTTP 規範，所有會修改資料庫狀態的操作（新增、切換、刪除、清理、編輯）皆使用 `POST` 方法，而非 `GET` 方法。操作完成後統一 `Redirect` 回首頁 `/` 以避免重新整理造成表單重複送出。
