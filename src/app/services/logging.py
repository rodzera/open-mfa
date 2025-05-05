import logging
from typing import Optional
from logging import getLevelName

from src.app.infra.logging import logging_infra
from src.app.configs.constants import PRODUCTION_ENV
from src.app.infra.signals import send_logging_signal
from src.app.utils.helpers.logging import get_logger
from src.app.repositories.logging import LoggingRepository

log = get_logger(__name__)


class LoggingService:
    """
    Controller and Application layer for logging service.
    """
    def __init__(self):
        self.repo = LoggingRepository()

    def get_level(self) -> Optional[dict]:
        log.info("Querying logging level")

        level = self.repo.get_level() or logging.root.level
        response = {"level": getLevelName(int(level))}

        log.debug(f"Returning logging level: {response}")
        return response

    def set_level(self, **req_data) -> dict:
        level = req_data["level"]
        int_level = getLevelName(level)

        log.debug(f"Updating logging level to: {level}")
        self.repo.set_level(int_level)

        if not PRODUCTION_ENV:
            logging_infra.set_level(int_level)
        else:
            send_logging_signal()

        log.info("Logging level updated successfully")
        return req_data
