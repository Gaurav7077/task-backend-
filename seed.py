import sys
import os
from sqlalchemy.sql import text


sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import db, create_app
from app.models.user import User
from app.models.task import TaskManager
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    
    db.session.execute(text('TRUNCATE TABLE "user" RESTART IDENTITY CASCADE'))
    db.session.execute(text('TRUNCATE TABLE "task_manager" RESTART IDENTITY CASCADE'))
    db.session.commit()

    
    users = [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password123', 'role': 'admin'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'password123', 'role': 'user'},
        {'username': 'user3', 'email': 'user3@example.com', 'password': 'password123', 'role': 'user'}
    ]
    created_user_ids = []
    for user in users:
        new_user = User(
            username=user['username'],
            email=user['email'],
            password=generate_password_hash(user['password']),
            role=user['role']
        )
        db.session.add(new_user)
    db.session.commit()

    
    created_users = User.query.all()
    created_user_ids = [user.id for user in created_users]

    
    if len(created_user_ids) >= 3:  
        db.session.execute(text("ALTER SEQUENCE task_manager_id_seq RESTART WITH 101"))
        db.session.commit()
        tasks = [
            {'id': 101, 'title': 'Complete Project', 'is_active': True, 'created_by': created_user_ids[0]},  
            {'id': 102, 'title': 'Write Docs', 'is_active': False, 'created_by': created_user_ids[1]},     
            {'id': 103, 'title': 'Test App', 'is_active': True, 'created_by': created_user_ids[2]}         
        ]
        for task in tasks:
            new_task = TaskManager(
                id=task['id'],
                title=task['title'],
                is_active=task['is_active'],
                created_by=task['created_by']
            )
            db.session.add(new_task)
        db.session.commit()

print("Database seeding completed successfully!")