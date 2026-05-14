from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# 初始化資料庫
with app.app_context():
    database.init_db()

@app.route('/')
def index():
    """
    任務列表 (首頁)
    取得所有代辦事項並渲染 index.html
    """
    tasks = database.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    """
    新增任務
    接收表單提交的 title，寫入資料庫後重導向回首頁
    """
    title = request.form.get('title')
    if title and title.strip():
        database.add_task(title.strip())
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
