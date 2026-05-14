import sqlite3
from flask import current_app

class TaskModel:
    @staticmethod
    def get_db_connection():
        """取得資料庫連線"""
        conn = sqlite3.connect(current_app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def get_all_tasks():
        """取得所有任務，依建立時間排序"""
        try:
            with TaskModel.get_db_connection() as conn:
                tasks = conn.execute(
                    'SELECT * FROM tasks ORDER BY created_at DESC'
                ).fetchall()
                return tasks
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def create_task(title):
        """新增一筆任務"""
        try:
            with TaskModel.get_db_connection() as conn:
                conn.execute(
                    'INSERT INTO tasks (title) VALUES (?)',
                    (title,)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def toggle_task_status(task_id):
        """反轉任務完成狀態"""
        try:
            with TaskModel.get_db_connection() as conn:
                task = conn.execute('SELECT is_completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
                if task:
                    new_status = 0 if task['is_completed'] else 1
                    conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_status, task_id))
                    conn.commit()
                    return True
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def delete_task(task_id):
        """刪除指定任務"""
        try:
            with TaskModel.get_db_connection() as conn:
                conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
