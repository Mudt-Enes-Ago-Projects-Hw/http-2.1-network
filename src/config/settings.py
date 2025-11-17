import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('JWT_SECRET')
    JWT_SECRET = os.getenv('JWT_SECRET')
    PORT = int(os.getenv('PORT', 5000))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.getenv('SQLITE_DB', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False