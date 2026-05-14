import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'daily_todo.db')

def get_db_connection():
    """取得資料庫連線"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以用字典方式存取欄位
    return conn

def init_db():
    """初始化資料庫 (執行 schema.sql)"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    with open('schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_all_tasks():
    """取得所有任務，按建立時間排序"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return tasks

def add_task(title):
    """新增一筆任務"""
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()

def toggle_task_status(task_id):
    """切換任務的完成狀態 (0 -> 1, 1 -> 0)"""
    conn = get_db_connection()
    # 先取得目前的狀態
    task = conn.execute('SELECT is_completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task:
        new_status = 0 if task['is_completed'] else 1
        conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
    conn.close()

def delete_task(task_id):
    """刪除任務"""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def update_task_title(task_id, new_title):
    """更新任務標題"""
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET title = ? WHERE id = ?', (new_title, task_id))
    conn.commit()
    conn.close()
