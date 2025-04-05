import os
from tenacity import retry, stop_after_attempt, wait_fixed

def init_db(app, db):
    # Debug: Print environment variables
    print("DB_USER:", os.getenv('DB_USER'))
    print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
    print("DB_HOST:", os.getenv('DB_HOST'))
    print("DB_NAME:", os.getenv('DB_NAME'))
    print("SQLALCHEMY_DATABASE_URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    app.config["SQLALCHEMY_POOL_SIZE"] = 10
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def connect_db():
        engine = db.engine
        engine.connect()
        return engine
    
    with app.app_context():
        try:
            connect_db()
            print("Database connection successful!")
            db.create_all()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise