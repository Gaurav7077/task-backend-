
from app import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    def __init__(self, username, email, password, role,id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role