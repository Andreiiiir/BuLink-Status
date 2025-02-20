from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import Config 

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
load_dotenv()

def create_app():

    app = Flask (__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from .auth.models import User
        from .main.models import Collaborator, Project, Note

        db.create_all()


    return app


from .auth.models import User
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))