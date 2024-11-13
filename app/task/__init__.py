from flask import Blueprint

blueprint = Blueprint("task", __name__, template_folder="templates")

from . import routes
