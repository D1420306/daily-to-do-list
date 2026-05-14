from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.models.task import TaskModel

# 建立名為 'tasks' 的 Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def index():
    """
    顯示任務列表首頁，包含新增任務的表單。
    """
    tasks = TaskModel.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/tasks/create', methods=['POST'])
def create_task():
    """
    接收表單資料，建立新任務，然後重導向回首頁。
    """
    title = request.form.get('title', '').strip()
    if not title:
        flash('任務名稱不能為空！', 'danger')
    else:
        success = TaskModel.create_task(title)
        if success:
            flash('任務新增成功！', 'success')
        else:
            flash('任務新增失敗，請稍後再試。', 'danger')
            
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    切換指定任務的完成狀態（待辦 <-> 已完成），然後重導向回首頁。
    """
    success = TaskModel.toggle_task_status(id)
    if not success:
        flash('狀態更新失敗，找不到該任務或資料庫錯誤。', 'danger')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除指定的任務，然後重導向回首頁。
    """
    success = TaskModel.delete_task(id)
    if success:
        flash('任務已刪除！', 'success')
    else:
        flash('刪除失敗，找不到該任務或資料庫錯誤。', 'danger')
    return redirect(url_for('tasks.index'))
