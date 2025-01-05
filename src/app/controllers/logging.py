from logging import getLevelName
from typing import Dict, Optional

from src.app.infra.logging import logging_service
from src.app.infra.signals import send_logging_signal
from src.app.repositories.logging import LoggingRepository


class LoggingController:

    @staticmethod
    def get_app_logging_level() -> Optional[Dict]:
        if int_level := LoggingRepository.get_app_logging_level():
            str_level = getLevelName(int(int_level))
            return {"level": str_level}

    @staticmethod
    def process_logging_request(level: str) -> None:
        int_level = getLevelName(level)
        LoggingRepository.set_app_logging_level(int_level)
        logging_service.set_logger_level(int_level)
        send_logging_signal()
