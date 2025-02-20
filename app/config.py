import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///BuLink&Status.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
