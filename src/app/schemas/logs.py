from marshmallow import post_load
from marshmallow.validate import OneOf

from src.app.schemas import ma
from src.app.utils.helpers.logs import get_logger
from src.app.services.logs import logging_service

log = get_logger(__name__)


class LogSchema(ma.Schema):
    level = ma.String(
        required=True,
        validate=OneOf(list(logging_service.AVAILABLE_LOG_LEVELS.keys()))
    )

    @post_load
    def set_logger_level(self, data, **kwargs):
        logging_service.process_logging_request(data["level"])
        return data
