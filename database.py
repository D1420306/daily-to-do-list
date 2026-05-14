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
