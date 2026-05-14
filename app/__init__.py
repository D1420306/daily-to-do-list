import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 載入環境變數設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
    
    # 確保 instance 資料夾存在 (用來放 database.db)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes.task_routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
