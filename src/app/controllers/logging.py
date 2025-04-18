from logging import getLevelName
from typing import Dict, Optional

from src.app.infra.logging import logging_service
from src.app.infra.signals import send_logging_signal
from src.app.repositories.logging import LoggingRepository


class LoggingController:
    def __init__(self):
        self.repository = LoggingRepository()

    def get_app_logging_level(self) -> Optional[Dict]:
        if int_level := self.repository.get_app_logging_level():
            str_level = getLevelName(int(int_level))
            return {"level": str_level}

    def process_logging_request(self, level: str) -> None:
        int_level = getLevelName(level)
        self.repository.set_app_logging_level(int_level)
        logging_service.set_logger_level(int_level)
        send_logging_signal()
