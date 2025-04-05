from flask import Blueprint, request, jsonify
from app.models.task import TaskManager, TaskLogger, db
from app.services.task_service import create_task, soft_delete_task, check_permission
from pydantic import BaseModel, ValidationError
import redis
from functools import wraps

tasks_bp = Blueprint("tasks", __name__)
r = redis.Redis(host="redis", port=6379, db=0)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").strip()
        print(f"Received token: '{token}'")  # Debugging
        expected_token = "Bearer secret"
        print(f"Expected token: '{expected_token}'")
        if not token:
            print("Token missing")
            return jsonify({"message": "Token missing"}), 401
        if token != expected_token:
            print("Token validation failed")
            return jsonify({"message": "Invalid token"}), 401
        print("Token validation passed")
        return f(*args, **kwargs)
    return decorated

class TaskInput(BaseModel):
    title: str

@tasks_bp.route("/upload-csv", methods=["POST"])
@token_required
def upload_csv():
    file = request.files["file"]
    
    return jsonify({"message": "CSV uploaded"}), 200

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    page = request.args.get("page", 1, type=int)
    tasks = TaskLogger.query.paginate(page=page, per_page=10)
    return jsonify([{"id": t.id, "task_id": t.task_id, "status": t.status} for t in tasks.items])

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks_by_date():
    date = request.args.get("date")
    cache_key = f"tasks:{date}"
    cached = r.get(cache_key)
    if cached:
        return jsonify(cached.decode())
    tasks = TaskLogger.query.filter_by(log_date=date).all()
    result = [{"id": t.id, "task_id": t.task_id} for t in tasks]
    r.setex(cache_key, 3600, jsonify(result).get_data())
    return jsonify(result)

@tasks_bp.route("/task/<int:task_logger_id>", methods=["GET"])
def get_task(task_logger_id):
    task = TaskLogger.query.get_or_404(task_logger_id)
    return jsonify({"id": task.id, "task_id": task.task_id, "status": task.status})

@tasks_bp.route("/task", methods=["POST"])
@token_required
def create_new_task():
    try:
        data = TaskInput(**request.json)
        task = create_task(data.title, user_id=1)  
        return jsonify({"id": task.id, "title": task.title}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

@tasks_bp.route("/task/<int:task_id>", methods=["PUT"])
@token_required
def update_task(task_id):
    check_permission(user_id=1, task_id=task_id)  
    task = TaskManager.query.get_or_404(task_id)
    data = request.json
    task.title = data.get("title", task.title)
    db.session.commit()
    return jsonify({"message": "Task updated"})

@tasks_bp.route("/task/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(task_id):
    soft_delete_task(task_id, user_id=1)  
    return jsonify({"message": "Task deleted"})