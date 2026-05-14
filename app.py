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

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    """
    切換任務完成狀態
    根據 task_id 切換 is_completed 欄位，完成後重導向回首頁
    """
    database.toggle_task_status(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    """
    刪除任務
    根據 task_id 刪除該筆資料，完成後重導向回首頁
    """
    database.delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    """
    編輯任務
    根據 task_id 更新 title 欄位，完成後重導向回首頁
    """
    new_title = request.form.get('new_title')
    if new_title and new_title.strip():
        database.update_task_title(task_id, new_title.strip())
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
