# 流程圖設計 (Flowchart)

## 1. 使用者流程圖 (User Flow)
這份流程圖描述了使用者進入「每日代辦事項」網站後，可能的操作路徑與交互體驗。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 任務列表]
    
    B --> C{選擇操作}
    
    C -->|輸入文字點擊新增| D[提交新增表單]
    D --> E[系統寫入任務資料]
    E --> B
    
    C -->|點擊任務勾選框| F[提交狀態切換請求]
    F -->|若是待辦則改為已完成\n若是已完成則改為待辦| G[系統更新任務狀態]
    G --> B
    
    C -->|點擊刪除按鈕| H[提交刪除請求]
    H --> I[系統刪除任務]
    I --> B
```

## 2. 系統序列圖 (Sequence Diagram)
這份序列圖以最核心的「標記完成/未完成」功能為例，描述了瀏覽器、Flask 後端與 SQLite 資料庫之間的完整溝通流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Task Model
    participant DB as SQLite DB

    User->>Browser: 點擊任務的勾選框
    Browser->>Route: POST /tasks/{id}/toggle
    Route->>Model: 呼叫 toggle_status(id)
    Model->>DB: UPDATE tasks SET status = ? WHERE id = ?
    DB-->>Model: 回傳成功
    Model-->>Route: 狀態更新完畢
    Route-->>Browser: HTTP 302 Redirect 回首頁 (/)
    Browser->>Route: GET /
    Route->>Model: 取得所有任務 (含新狀態)
    Model->>DB: SELECT * FROM tasks
    DB-->>Model: 回傳任務列表
    Model-->>Route: 任務列表資料
    Route-->>Browser: 渲染 index.html (顯示更新後的勾選狀態)
    Browser-->>User: 看到任務狀態已變更
```

## 3. 功能清單對照表
統整所有操作與對應的路由端點：

| 功能操作 | HTTP 方法 | URL 路徑 | 對應流程結果 |
| :--- | :---: | :--- | :--- |
| **檢視首頁** | `GET` | `/` | 顯示所有任務的列表 |
| **新增任務** | `POST` | `/tasks` | 寫入資料後重導向至 `/` |
| **切換狀態** | `POST` | `/tasks/<id>/toggle` | 更新狀態後重導向至 `/` |
| **刪除任務** | `POST` | `/tasks/<id>/delete` | 刪除資料後重導向至 `/` |
