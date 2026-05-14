# ARCHITECTURE: 每日代辦 (Daily To-Do List) 系統架構設計

## 1. 技術架構說明

本專案將採用輕量級的後端框架與伺服器渲染技術，以快速建立 MVP 並滿足需求：

- **後端框架**：Python + Flask
  - **原因**：Flask 是輕量、靈活的微框架，適合建置小型應用如代辦清單。
- **模板引擎**：Jinja2
  - **原因**：內建於 Flask，可直接在後端將資料注入 HTML 模板並渲染，減少初期建置前後端分離（如 React/Vue）的複雜度。
- **資料庫**：SQLite + Flask-SQLAlchemy
  - **原因**：SQLite 是單檔資料庫，無需安裝額外的資料庫伺服器（如 MySQL 或 PostgreSQL），非常適合單一使用者的輕量級應用與本機開發。使用 SQLAlchemy ORM 可以簡化 SQL 語法操作。
- **前端樣式**：純 CSS (Vanilla CSS)
  - **原因**：不依賴過多框架，專注於提供現代化視覺效果（如深色模式、Glassmorphism），維持輕量且高效。

### Flask MVC 模式對應
- **Model (模型)**：定義資料結構（如 `Task` 包含 `id`, `title`, `is_completed` 等屬性），負責與 SQLite 資料庫互動。
- **View (視圖)**：Jinja2 HTML 模板，負責將 Controller 傳遞過來的資料渲染成使用者可以看到的網頁。
- **Controller (控制器)**：Flask 的 Route 函式，負責接收使用者的 HTTP 請求（如 GET 列表、POST 新增任務）、呼叫 Model 取得或更新資料，最後回傳對應的 View。

## 2. 專案資料夾結構

```text
daily-to-do-list/
├── app/                  # 應用程式核心目錄
│   ├── __init__.py       # 初始化 Flask App 與套件 (如 SQLAlchemy)
│   ├── models.py         # 資料庫模型 (Task Model)
│   ├── routes.py         # URL 路由與商業邏輯 (新增、刪除、切換狀態等)
│   ├── templates/        # Jinja2 HTML 模板
│   │   └── index.html    # 主要任務列表頁面
│   └── static/           # 靜態資源檔案
│       └── css/
│           └── style.css # 核心樣式表 (現代化設計、深色模式)
├── instance/             # 存放本地端產生的檔案 (不會被提交至 Git)
│   └── database.db       # SQLite 資料庫檔案
├── docs/                 # 專案設計文件
│   ├── PRD.md
│   └── ARCHITECTURE.md
├── requirements.txt      # Python 相依套件清單
└── run.py                # 專案啟動入口程式
```

## 3. 元件關係圖

```mermaid
flowchart TD
    Browser[瀏覽器 (Client)] -->|HTTP GET/POST| Route[Flask Routes (app/routes.py)]
    Route -->|CRUD Operations| Model[SQLAlchemy Models (app/models.py)]
    Model -->|Read/Write| SQLite[(SQLite Database)]
    SQLite -.->|Data| Model
    Model -.->|Objects| Route
    Route -->|Pass Data| Template[Jinja2 Templates (app/templates/)]
    Template -->|Render HTML| Browser
```

## 4. 關鍵設計決策

1. **單頁面應用體驗 (SPA-like feel with SSR)**：
   我們將大部分操作（新增、切換狀態、刪除）集中在單一首頁 (`index.html`)。雖然使用後端渲染 (SSR)，但我們會優化路由的重新導向，讓使用者操作後能快速看見狀態更新。
2. **採用 Flask-SQLAlchemy 替代原生 sqlite3**：
   原生的 sqlite3 容易寫出不易維護的 SQL 字串。導入 Flask-SQLAlchemy 這個 ORM 工具，可以讓我們以 Python 物件的方式操作資料表，減少 SQL Injection 風險，且日後若需遷移至 PostgreSQL 等其他資料庫也極為容易。
3. **前端視覺先行**：
   根據 PRD，雖然是基礎 CRUD，但需要現代化與「Wow」的設計體驗。我們將在 `static/css/style.css` 投入較多心力處理變數設定 (CSS Variables)、深色主題、漸層背景與微動畫，讓它不僅是一個功能 MVP，也是一個質感 MVP。
