from app import db
from datetime import datetime


class TaskManager(db.Model):
    __tablename__ = "task_manager"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))

class TaskLogger(db.Model):
    __tablename__ = "task_logger"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task_manager.id", ondelete="CASCADE"))
    status = db.Column(db.String(20), default="pending")
    log_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)