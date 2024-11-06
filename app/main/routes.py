import logging
from . import blueprint

logger = logging.getLogger(__name__)


@blueprint.route("/test")
def index():
    return "Endpoint respoding successfully"
