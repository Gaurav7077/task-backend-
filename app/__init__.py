import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config.database import init_db

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    
    init_db(app, db)
    
    
    from app.models.task import TaskManager, TaskLogger
    from app.models.user import User
    
    
    from app.routes import task_bp
    app.register_blueprint(task_bp, url_prefix='/api')
    
    return app

app = create_app()
from app.celery import make_celery
celery = make_celery(app)