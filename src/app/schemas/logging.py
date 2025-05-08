from marshmallow.validate import OneOf

from src.app.schemas import ma
from src.infra.logging import logging_infra
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class LoggingSchema(ma.Schema):
    level = ma.String(
        required=True,
        validate=OneOf(list(logging_infra.AVAILABLE_LOG_LEVELS.keys()))
    )
