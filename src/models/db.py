from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_tables():
    from src.models.user import User
    from src.models.blog import Blog
    db.create_all()