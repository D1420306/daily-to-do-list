# 系統架構設計 (Architecture)

## 1. 技術架構說明
本專案採用 **MVC (Model-View-Controller)** 架構模式來組織程式碼：
- **選用技術與原因**：
  - **Python + Flask**：輕量級的後端框架，適合快速開發小型與中型應用。
  - **Jinja2**：Flask 內建的模板引擎，可直接在 HTML 中嵌入 Python 變數與邏輯，適合不分離前後端的快速開發。
  - **SQLite**：輕量級關聯式資料庫，無需額外安裝伺服器軟體，資料存放在本地檔案，十分適合 MVP 階段。
  - **Bootstrap 5 (Frontend)**：快速打造美觀且具備響應式 (RWD) 的介面，無須從零撰寫大量 CSS。

- **Flask MVC 模式說明**：
  - **Model (模型)**：負責與資料庫 (SQLite) 溝通，處理資料的 CRUD 邏輯（例如：寫入新任務、更新狀態）。
  - **View (視圖)**：負責呈現使用者介面，使用 Jinja2 渲染 HTML 模板，並將資料呈現給使用者。
  - **Controller (控制器)**：在 Flask 中由路由 (Routes) 擔任，負責接收使用者的 HTTP 請求 (GET/POST)，驗證資料，呼叫對應的 Model，最後決定要渲染哪一個 View 或進行重導向 (Redirect)。

## 2. 專案資料夾結構

```text
daily-to-do-list/
├── app/
│   ├── __init__.py        # Flask 應用程式工廠與初始化
│   ├── models/            # Model 層：資料庫操作
│   │   └── task.py        # Task 資料表的操作邏輯
│   ├── routes/            # Controller 層：路由邏輯
│   │   └── task_routes.py # 任務相關的 API / 路由
│   ├── templates/         # View 層：Jinja2 模板
│   │   ├── base.html      # 基礎共同版型
│   │   └── index.html     # 任務列表與新增表單
│   └── static/            # 靜態資源檔案
│       ├── css/
│       │   └── style.css  # 自訂樣式
│       └── js/
│           └── main.js    # 自訂前端邏輯 (例如非同步狀態切換)
├── database/
│   └── schema.sql         # SQLite 建表語法
├── instance/
│   └── database.db        # 執行時產生的 SQLite 資料庫檔案
├── docs/                  # 專案設計文件
├── .env.example           # 環境變數範例檔
├── requirements.txt       # Python 套件依賴清單
└── app.py                 # 專案啟動入口檔
```

## 3. 元件關係圖

```mermaid
flowchart LR
    Browser([瀏覽器]) <--> |1. HTTP GET / POST | Flask_Route[Flask Route\n(Controller)]
    Flask_Route <--> |2. 讀寫資料 | Model[Task Model\n(Model)]
    Model <--> |3. 執行 SQL | SQLite[(SQLite Database)]
    Flask_Route <--> |4. 準備資料 | Jinja2[Jinja2 Template\n(View)]
    Jinja2 --> |5. 渲染 HTML | Browser
```

## 4. 關鍵設計決策
1. **任務狀態切換機制的實作方式**：
   - 由於這是一個伺服器端渲染 (SSR) 的專案，當使用者點擊「勾選框」切換狀態時，可以採用傳統的表單 POST 提交 (會重新載入頁面) 或是透過輕量級的 JavaScript fetch 發送非同步請求 (體驗更平滑)。我們將優先使用**傳統表單 POST + 重導向**來維持基礎架構的單純性，若有進階體驗需求，再加入 JS 增強。
2. **資料庫存取方式**：
   - 使用原生的 `sqlite3` 模組搭配 `sqlite3.Row` factory。這樣可以免去設定 SQLAlchemy 的複雜度，保持系統輕量，同時也能使用字典語法存取資料列。
3. **沒有前端框架 (No SPA)**：
   - 專案定位為簡單快速的待辦事項，引入 React/Vue 會增加不必要的複雜度。Jinja2 + HTML 即可滿足所有需求。
