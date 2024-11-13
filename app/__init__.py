import os

from . import config

from flask import Flask
from flask_migrate import Migrate


migrate = Migrate()


def create_app(config_filename=None):
    from .models import db
    from .main import blueprint as main_blueprint
    from .auth import blueprint as auth_blueprint
    from .task import blueprint as task_blueprint

    app = Flask(__name__)
    config_filename = config_filename or config.DevConfig
    app.config.from_object(config_filename)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint, url_prefix="/main")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(task_blueprint, url_prefix="/task")
    app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    for rule in app.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        print(f"{rule.endpoint:30s} {methods:20s} {rule}")

    return app
