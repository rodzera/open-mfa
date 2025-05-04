import logging
from logging import getLevelName
from typing import Dict, Optional

from src.app.infra.logging import logging_service
from src.app.infra.signals import send_logging_signal
from src.app.configs.constants import PRODUCTION_ENV
from src.app.repositories.logging import LoggingRepository


class LoggingService:
    """
    Controller and Application layer for logging service.
    """
    def __init__(self):
        self.repo = LoggingRepository()

    def get_level(self) -> Optional[Dict]:
        int_level = self.repo.get_level()
        level = int_level or logging.root.level
        return {"level": getLevelName(int(level))}

    def set_level(self, **req_data) -> dict:
        level = req_data["level"]
        int_level = getLevelName(level)
        self.repo.set_level(int_level)

        if not PRODUCTION_ENV:
            logging_service.set_level(int_level)
        else:
            send_logging_signal()
        return req_data
