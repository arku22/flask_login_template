from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from flask_login import LoginManager
from flask_mail import Mail


# extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login_page"
mail = Mail()


def create_app(configname):

    app = Flask(__name__)
    app.config.from_object(config[configname])

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # register blueprints
    from .main import main
    app.register_blueprint(main, url_prefix="/")
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")
    from .user import user
    app.register_blueprint(user, url_prefix="/user")

    return app
