DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 預先插入測試資料，方便測試「任務內容編輯」功能
INSERT INTO tasks (title) VALUES ('學習如何使用 Fetch API');
INSERT INTO tasks (title) VALUES ('點擊我來測試編輯功能');
INSERT INTO tasks (title) VALUES ('設計具有高質感的 UI 互動');
