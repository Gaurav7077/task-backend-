from flask import Blueprint, request, jsonify
from app import db
from app.models.task import TaskManager, TaskLogger  
from app.models.user import User
from werkzeug.security import generate_password_hash
import pandas as pd
from datetime import datetime

task_bp = Blueprint('task', __name__)


@task_bp.route('/task', methods=['GET'])
def get_tasks():
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401
    
    tasks = TaskManager.query.all()
    tasks_list = [{'id': task.id, 'title': task.title, 'is_active': task.is_active, 'created_by': task.created_by} for task in tasks]
    return jsonify(tasks_list), 200


@task_bp.route('/task', methods=['POST'])
def create_task():
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    title = data.get('title')
    is_active = data.get('is_active', True)
    created_by = data.get('created_by', 1)
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    try:
        task = TaskManager(title=title, is_active=is_active, created_by=created_by)
        db.session.add(task)
        db.session.flush()  
        
        
        task_log = TaskLogger(task_id=task.id, status="pending", log_date=datetime.now())
        db.session.add(task_log)
        
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'is_active': task.is_active, 'created_by': task.created_by}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401
    
    task = TaskManager.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    title = data.get('title')
    is_active = data.get('is_active', task.is_active)
    created_by = data.get('created_by', task.created_by)
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    try:
        task.title = title
        task.is_active = is_active
        task.created_by = created_by
        
        
        task_log = TaskLogger(task_id=task.id, status="updated", log_date=datetime.now())
        db.session.add(task_log)
        
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'is_active': task.is_active, 'created_by': task.created_by}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401
    
    task = TaskManager.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        
        task_log = TaskLogger(task_id=task.id, status="deleted", log_date=datetime.now())
        db.session.add(task_log)
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        try:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                
                user = User.query.get(row['created_by'])
                if not user:
                    return jsonify({'error': f"User with ID {row['created_by']} does not exist"}), 400
                
                task = TaskManager(
                    
                    title=row['title'],
                    is_active=bool(row['is_active']),
                    created_by=int(row['created_by'])
                )
                db.session.add(task)
                db.session.flush()  
                
                
                task_log = TaskLogger(task_id=task.id, status="pending", log_date=datetime.now())
                db.session.add(task_log)
                
            db.session.commit()
            return jsonify({'message': 'CSV file uploaded and data inserted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file format'}), 400


@task_bp.route('/upload-task-logger-csv', methods=['POST'])
def upload_task_logger_csv():
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        try:
            df = pd.read_csv(file)
            
            required_columns = ['task_id', 'status']
            if not all(col in df.columns for col in required_columns):
                return jsonify({'error': f"Missing required columns. Required: {required_columns}"}), 400

            valid_statuses = ['pending', 'completed', 'failed']
            for _, row in df.iterrows():
                
                task = TaskManager.query.get(row['task_id'])
                if not task:
                    return jsonify({'error': f"Task with ID {row['task_id']} does not exist"}), 400
                
                
                if row['status'] not in valid_statuses:
                    return jsonify({'error': f"Invalid status: {row['status']}. Allowed values: {valid_statuses}"}), 400
                
                
                log_date = row.get('log_date')
                if log_date:
                    log_date = datetime.strptime(log_date, '%Y-%m-%d %H:%M:%S')
                else:
                    log_date = datetime.now()

                
                task_log = TaskLogger(
                    task_id=int(row['task_id']),
                    status=row['status'],
                    log_date=log_date
                )
                db.session.add(task_log)
            db.session.commit()
            return jsonify({'message': 'Task logger CSV file uploaded and data inserted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file format'}), 400


@task_bp.route('/user', methods=['POST'])
def create_user():
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer secret':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    id_value = data.get('id')  

    if not all([username, email, password, role]):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=username, email=email, password=password, role=role, id=id_value)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'id': user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500