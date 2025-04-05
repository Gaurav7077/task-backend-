from celery import Celery
from app import create_app, db
from app.models.task import TaskManager, TaskLogger
from datetime import datetime

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

app = create_app()
celery.conf.update(app.config)

@celery.task
def daily_task_loader():
    with app.app_context():
        active_tasks = TaskManager.query.filter_by(is_active=True).all()
        today = datetime.utcnow().date()
        for task in active_tasks:
            if not TaskLogger.query.filter_by(task_id=task.id, log_date=today).first():
                log = TaskLogger(task_id=task.id)
                db.session.add(log)
        db.session.commit()