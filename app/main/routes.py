import logging

from . import blueprint
from ..auth.helpers import auth_protected

logger = logging.getLogger(__name__)


@blueprint.route("/test")
@auth_protected
def index():
    return "Endpoint respoding successfully"
