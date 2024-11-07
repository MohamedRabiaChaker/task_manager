from flask import Flask
from . import config
from flask_migrate import Migrate

migrate = Migrate()


def create_app(config_filename=None):
    from .models import db
    from .main import blueprint as main_blueprint

    app = Flask(__name__)
    config_filename = config_filename or config.DevConfig
    app.config.from_object(config_filename)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint, url_prefix="/main")

    return app
