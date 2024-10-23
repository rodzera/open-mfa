from src.app.resources.api import api
from src.app.logger import get_logger
from src.app.configs.constants import VERSION
from src.app.utils.helpers.queries import get_db_timestamp
from src.app.utils.handlers.request import request_validator

log = get_logger(__name__)


@api.route("/database", methods=["GET"])
@request_validator()
def database():
    db_datetime = get_db_timestamp()
    return {"status": "up", "datetime": db_datetime} if db_datetime else {"status": "down"}


@api.route("/server", methods=["GET"])
@request_validator()
def server():
    return {"status": "up", "version": VERSION}
