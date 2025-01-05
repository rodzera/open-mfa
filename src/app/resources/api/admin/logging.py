from src.app.resources.api import api
from src.app.schemas.logging import LoggingSchema
from src.app.controllers.logging import LoggingController
from src.app.infra.middlewares.auth import auth_middleware
from src.app.infra.middlewares.schemas import schema_middleware


@api.route("/logging", methods=["GET"])
@auth_middleware
def get_logging_level():
    return LoggingController.get_app_logging_level()


@api.route("/logging", methods=["PUT"])
@auth_middleware
@schema_middleware(LoggingSchema)
def set_logging_level(**client_data):
    return client_data
