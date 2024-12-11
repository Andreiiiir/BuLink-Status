import os

class Config:
    # Load the secret key from the environment variable
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')  # fallback for local dev
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
