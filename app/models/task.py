"""
Task Model — 與 SQLite tasks 資料表互動的 CRUD 方法集。
"""
import sqlite3
import os
from datetime import datetime

DATABASE = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'database.db')


def get_db_connection():
    """建立並回傳一個 sqlite3 連線，row_factory 設為 sqlite3.Row。"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ── 優先順序對應設定（高/中/低 → CSS class 與中文標籤）──────────────────────
PRIORITY_CONFIG = {
    'high':   {'label': '高', 'css_class': 'priority-high',   'badge': 'badge-high'},
    'medium': {'label': '中', 'css_class': 'priority-medium', 'badge': 'badge-medium'},
    'low':    {'label': '低', 'css_class': 'priority-low',    'badge': 'badge-low'},
}


def create(title: str, description: str = '', priority: str = 'medium', due_date: str = '') -> int:
    """
    新增一筆任務記錄。
    :param title:       任務標題（必填）
    :param description: 任務描述
    :param priority:    優先順序 'high' | 'medium' | 'low'
    :param due_date:    到期日 YYYY-MM-DD
    :return:            新增記錄的 id
    """
    if priority not in PRIORITY_CONFIG:
        priority = 'medium'
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO tasks (title, description, priority, due_date, is_done, created_at) '
            'VALUES (?, ?, ?, ?, 0, ?)',
            (title, description, priority, due_date, datetime.now().isoformat())
        )
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except Exception as e:
        raise RuntimeError(f'create task failed: {e}') from e
    finally:
        conn.close()


def get_all() -> list:
    """
    取得所有任務，依優先順序（高→中→低）排序，未完成優先。
    :return: list of sqlite3.Row
    """
    try:
        conn = get_db_connection()
        tasks = conn.execute(
            '''SELECT * FROM tasks
               ORDER BY
                 is_done ASC,
                 CASE priority WHEN "high" THEN 1 WHEN "medium" THEN 2 ELSE 3 END,
                 due_date ASC NULLS LAST,
                 created_at ASC'''
        ).fetchall()
        return tasks
    except Exception as e:
        raise RuntimeError(f'get_all tasks failed: {e}') from e
    finally:
        conn.close()


def get_by_id(task_id: int):
    """
    依 id 取得單筆任務。
    :param task_id: 任務 id
    :return:        sqlite3.Row 或 None
    """
    try:
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return task
    except Exception as e:
        raise RuntimeError(f'get_by_id task failed: {e}') from e
    finally:
        conn.close()


def update(task_id: int, title: str, description: str = '', priority: str = 'medium', due_date: str = '') -> None:
    """
    更新指定任務的內容。
    :param task_id:     任務 id
    :param title:       新標題
    :param description: 新描述
    :param priority:    新優先順序 'high' | 'medium' | 'low'
    :param due_date:    新到期日
    """
    if priority not in PRIORITY_CONFIG:
        priority = 'medium'
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET title=?, description=?, priority=?, due_date=? WHERE id=?',
            (title, description, priority, due_date, task_id)
        )
        conn.commit()
    except Exception as e:
        raise RuntimeError(f'update task failed: {e}') from e
    finally:
        conn.close()


def delete(task_id: int) -> None:
    """
    刪除指定任務。
    :param task_id: 任務 id
    """
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    except Exception as e:
        raise RuntimeError(f'delete task failed: {e}') from e
    finally:
        conn.close()


def toggle_done(task_id: int) -> None:
    """
    切換任務的完成狀態（0 ↔ 1）。
    :param task_id: 任務 id
    """
    try:
        conn = get_db_connection()
        conn.execute('UPDATE tasks SET is_done = 1 - is_done WHERE id = ?', (task_id,))
        conn.commit()
    except Exception as e:
        raise RuntimeError(f'toggle_done failed: {e}') from e
    finally:
        conn.close()
