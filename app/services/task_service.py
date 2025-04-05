from app import db  # Import db from app/__init__.py
from app.models.task import TaskManager, TaskLogger, User

def check_permission(user_id, task_id):
    user = User.query.get(user_id)
    task = TaskManager.query.get(task_id)
    if user.role != "admin" and task.created_by != user_id:
        raise PermissionError("Unauthorized")

def create_task(title, user_id):
    task = TaskManager(title=title, created_by=user_id)
    db.session.add(task)
    db.session.commit()
    return task

def soft_delete_task(task_id, user_id):
    check_permission(user_id, task_id)
    task = TaskManager.query.get(task_id)
    task.is_active = False
    db.session.commit()