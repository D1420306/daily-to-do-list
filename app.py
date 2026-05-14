from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    """建立 SQLite 資料庫連線並回傳 connection 物件"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫與測試資料"""
    if not os.path.exists(DATABASE):
        with app.app_context():
            conn = get_db_connection()
            with open('schema.sql', 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()

# 程式啟動時確保資料庫存在
init_db()

@app.route('/', methods=['GET'])
def index():
    """
    載入首頁並顯示所有任務。
    """
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    更新特定任務的內容 (Title)。
    前端會透過 Fetch API 發送 JSON 格式的請求。
    """
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"success": False, "error": "Invalid input"}), 400
    
    new_title = data['title'].strip()
    if not new_title:
        return jsonify({"success": False, "error": "Title cannot be empty"}), 400

    conn = get_db_connection()
    # 檢查任務是否存在
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({"success": False, "error": "Task not found"}), 404

    # 執行更新
    conn.execute('UPDATE tasks SET title = ? WHERE id = ?', (new_title, id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "title": new_title})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
