from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config


# extensions
db = SQLAlchemy()


def create_app(configname):

    app = Flask(__name__)
    app.config.from_object(config[configname])

    # init extensions
    db.init_app(app)

    # register blueprints
    from .auth import auth
    app.register_blueprint(auth)

    return app
