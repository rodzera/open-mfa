from datetime import datetime

from src.app.utils.helpers.logs import get_logger
from src.app.resources.api import api
from src.app.configs.constants import VERSION
from src.app.infra.middlewares.auth import admin_auth
from src.app.infra.redis import redis_service

log = get_logger(__name__)


@api.route("/database", methods=["GET"])
@admin_auth()
def database():
    db_datetime = redis_service.current_timestamp
    return {
        "status": "up",
        "datetime": db_datetime,
        "version": redis_service.info.get("redis_version", "unknown")
    } if db_datetime else {
        "status": "down"
    }


@api.route("/server", methods=["GET"])
@admin_auth()
def server():
    return {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "up",
        "version": VERSION
    }
