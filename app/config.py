import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/TestDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Darynka'  # Used for session encryption
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessions')
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SAMESITE = None
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_NAME = 'session'