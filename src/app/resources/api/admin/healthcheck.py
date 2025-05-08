from src.app.resources.api import api
from src.app.utils.helpers.logging import get_logger
from src.app.middlewares.auth import auth_middleware
from src.app.services.healthcheck import HealthCheckService

log = get_logger(__name__)


@api.route("/database", methods=["GET"])
@auth_middleware
def database_healthcheck():
    return HealthCheckService().get_db_status()


@api.route("/server", methods=["GET"])
@auth_middleware
def server_healthcheck():
    return HealthCheckService().get_server_status()
