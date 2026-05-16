"""
tasks Blueprint — 處理所有代辦事項相關的 Flask 路由。
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import task as Task
from app.models.task import PRIORITY_CONFIG

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
def index():
    """首頁：顯示所有任務列表，依優先順序排序。"""
    tasks = Task.get_all()
    total  = len(tasks)
    done   = sum(1 for t in tasks if t['is_done'])
    return render_template(
        'tasks/index.html',
        tasks=tasks,
        total=total,
        done=done,
        priority_config=PRIORITY_CONFIG
    )


@tasks_bp.route('/tasks/new')
def new_task():
    """顯示新增任務表單。"""
    return render_template('tasks/new.html', priority_config=PRIORITY_CONFIG)


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """接收新增任務表單，存入資料庫後重導向首頁。"""
    title       = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority    = request.form.get('priority', 'medium')
    due_date    = request.form.get('due_date', '').strip()

    if not title:
        flash('任務標題不能為空！', 'error')
        return redirect(url_for('tasks.new_task'))

    if priority not in PRIORITY_CONFIG:
        priority = 'medium'

    try:
        Task.create(title, description, priority, due_date)
        flash(f'任務「{title}」已成功新增！', 'success')
    except Exception as e:
        flash(f'新增失敗：{e}', 'error')

    return redirect(url_for('tasks.index'))


@tasks_bp.route('/tasks/<int:task_id>/edit')
def edit_task(task_id):
    """顯示編輯任務表單，預填現有資料。"""
    task = Task.get_by_id(task_id)
    if task is None:
        flash('找不到該任務。', 'error')
        return redirect(url_for('tasks.index'))
    return render_template('tasks/edit.html', task=task, priority_config=PRIORITY_CONFIG)


@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """接收編輯表單，更新資料庫後重導向首頁。"""
    title       = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority    = request.form.get('priority', 'medium')
    due_date    = request.form.get('due_date', '').strip()

    if not title:
        flash('任務標題不能為空！', 'error')
        return redirect(url_for('tasks.edit_task', task_id=task_id))

    if priority not in PRIORITY_CONFIG:
        priority = 'medium'

    try:
        Task.update(task_id, title, description, priority, due_date)
        flash(f'任務「{title}」已更新！', 'success')
    except Exception as e:
        flash(f'更新失敗：{e}', 'error')

    return redirect(url_for('tasks.index'))


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """刪除指定任務後重導向首頁。"""
    try:
        task = Task.get_by_id(task_id)
        title = task['title'] if task else ''
        Task.delete(task_id)
        flash(f'任務「{title}」已刪除。', 'success')
    except Exception as e:
        flash(f'刪除失敗：{e}', 'error')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """切換任務完成狀態（完成 ↔ 未完成）。"""
    try:
        Task.toggle_done(task_id)
    except Exception as e:
        flash(f'操作失敗：{e}', 'error')
    return redirect(url_for('tasks.index'))
