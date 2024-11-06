import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_filename=None):
    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)

    from .main import blueprint as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/main")

    return app
