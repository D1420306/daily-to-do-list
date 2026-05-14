# 流程圖設計 - 每日代辦事項 (Daily To-Do List)

## 1. 使用者流程圖 (User Flow)

這張圖描述了使用者進入網站後可以執行的各種操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 任務列表]
    
    Home --> Action{要執行什麼操作？}
    
    Action -->|輸入文字並送出| Add[新增任務]
    Add -->|重新載入| Home
```

## 2. 系統序列圖 (Sequence Diagram)

這裡我們以「新增任務」為例，展示從使用者點擊送出到資料寫入資料庫的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask 路由
    participant DB as SQLite 資料庫
    
    User->>Browser: 填寫代辦事項並送出表單
    Browser->>Route: POST /add (帶有文字資料)
    
    Route->>Route: 驗證輸入文字是否為空
    
    alt 輸入為空
        Route-->>Browser: 重導回首頁 (或顯示錯誤)
    else 輸入有效
        Route->>DB: INSERT INTO tasks (title)
        DB-->>Route: 寫入成功
        Route-->>Browser: 重導向 (Redirect) 到首頁 (GET /)
    end
    
    Browser->>Route: GET / (重新請求首頁)
    Route->>DB: SELECT * FROM tasks
    DB-->>Route: 回傳最新任務列表
    Route-->>Browser: 渲染包含新任務的 HTML 頁面
```

## 3. 功能清單對照表

以下是系統所有功能與其對應的 URL 路徑與 HTTP 方法：

| 功能描述 | HTTP 方法 | URL 路徑 | 說明 |
| --- | --- | --- | --- |
| 檢視任務清單 | GET | `/` | 載入首頁並顯示所有任務 |
| 新增任務 | POST | `/add` | 接收表單資料，寫入後重導向回首頁 |
