import sqlite3
import os
from flask import Flask
from app.routes.tasks import tasks_bp

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
SCHEMA   = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')


def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.secret_key = 'daily-todo-secret-key-2024'

    app.register_blueprint(tasks_bp)

    with app.app_context():
        init_db()

    return app


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = get_db_connection()
    with open(SCHEMA, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
