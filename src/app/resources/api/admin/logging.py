from src.app.resources.api import api
from src.app.schemas.logging import LoggingSchema
from src.app.services.logging import LoggingService
from src.app.infra.middlewares.auth import auth_middleware
from src.app.infra.middlewares.schemas import schema_middleware


@api.route("/logging", methods=["GET"])
@auth_middleware
def get_logging_level():
    return LoggingService().get_level()


@api.route("/logging", methods=["PUT"])
@auth_middleware
@schema_middleware(LoggingSchema)
def set_logging_level(**req_data):
    return LoggingService().set_level(**req_data)
