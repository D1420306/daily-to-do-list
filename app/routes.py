from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Task

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Order by created_at descending
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    # Split into incomplete and complete
    incomplete_tasks = [t for t in tasks if not t.is_completed]
    completed_tasks = [t for t in tasks if t.is_completed]
    return render_template('index.html', incomplete_tasks=incomplete_tasks, completed_tasks=completed_tasks)

@main_bp.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    if not title:
        flash('任務名稱不能為空', 'error')
        return redirect(url_for('main.index'))
    
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    flash('成功新增任務！', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_completed = not task.is_completed
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('任務已刪除', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    title = request.form.get('title', '').strip()
    if title:
        task.title = title
        db.session.commit()
        flash('任務已更新', 'success')
    else:
        flash('任務名稱不能為空', 'error')
    return redirect(url_for('main.index'))

@main_bp.route('/clear-completed', methods=['POST'])
def clear_completed():
    completed_tasks = Task.query.filter_by(is_completed=True).all()
    for task in completed_tasks:
        db.session.delete(task)
    db.session.commit()
    flash('已清理完成的任務', 'success')
    return redirect(url_for('main.index'))
