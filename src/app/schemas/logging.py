from marshmallow import post_load
from marshmallow.validate import OneOf

from src.app.schemas import ma
from src.app.infra.logging import logging_service
from src.app.utils.helpers.logging import get_logger
from src.app.controllers.logging import LoggingController

log = get_logger(__name__)


class LoggingSchema(ma.Schema):
    level = ma.String(
        required=True,
        validate=OneOf(list(logging_service.AVAILABLE_LOG_LEVELS.keys()))
    )

    @post_load
    def set_logger_level(self, data, **kwargs):
        LoggingController().process_logging_request(data["level"])
        return data
