from app import create_app
import sqlite3
import os

app = create_app()

def init_db():
    """初始化資料庫與資料表"""
    db_path = app.config['DATABASE']
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    # 確保資料夾存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print("資料庫初始化完成！")

if __name__ == '__main__':
    app.run(debug=True)
