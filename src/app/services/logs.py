import logging
from logging import StreamHandler
from typing import Dict
from os import path, mkdir
from logging.handlers import TimedRotatingFileHandler

from src.app.services.redis import redis_service
from src.app.services.signals import send_logging_signal
from src.app.configs.constants import TESTING_ENV, DEVELOPMENT_ENV


class LoggingService(object):
    DEFAULT_DIR: str = "logs"
    DEFAULT_LEVEL: int = logging.DEBUG if DEVELOPMENT_ENV else logging.INFO
    AVAILABLE_LOG_LEVELS: Dict = {
        k: v for k, v in logging._nameToLevel.items() if v != logging.NOTSET
    }
    DEFAULT_LOGGERS: Dict = {
        "open-mfa": "logs/app.log",
        "redis": "logs/redis.log",
        "werkzeug": "logs/server.log"
    }

    def __init__(self):
        self.handlers = []
        self.formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(funcName)s | %(lineno)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def configure_loggers(self) -> None:
        self._add_stream_handler()
        self._add_file_handlers()
        logging.basicConfig(level=self.DEFAULT_LEVEL, handlers=self.handlers)

    def _add_stream_handler(self) -> None:
        sh = logging.StreamHandler()
        sh.setLevel(self.DEFAULT_LEVEL)
        sh.setFormatter(self.formatter)
        self.handlers.append(sh)
        for logger_name in self.DEFAULT_LOGGERS.keys():
            self._add_handler_to_logger(logger_name, sh)

    def _add_file_handlers(self) -> None:
        if not TESTING_ENV:
            if not path.exists("logs"):
                mkdir("logs")

            for logger_name, log_file in self.DEFAULT_LOGGERS.items():
                file_handler = TimedRotatingFileHandler(
                    log_file, when="d", interval=1, backupCount=30
                )
                file_handler.setLevel(self.DEFAULT_LEVEL)
                file_handler.setFormatter(self.formatter)
                self.handlers.append(file_handler)
                self._add_handler_to_logger(logger_name, file_handler)

    @staticmethod
    def _add_handler_to_logger(logger_name: str, handler: logging.Handler) -> None:
        logger = logging.getLogger(logger_name)
        if handler not in logger.handlers:
            logger.addHandler(handler)
        logger.propagate = False
        logger.addHandler(handler)

    def set_logger_level(self, level: int) -> None:
        logging.root.level = level
        for name in logging.root.manager.loggerDict:
            if any(name.startswith(prefix) for prefix in self.DEFAULT_LOGGERS.keys()):
                logger = logging.getLogger(name)
                logger.setLevel(level)
                for handler in logger.handlers:
                    handler.setLevel(level)

    def process_logging_request(self, level: str) -> None:
        int_level = logging._nameToLevel[level]
        redis_service.db("set", "log", int_level)
        self.set_logger_level(int_level)
        send_logging_signal()

logging_service = LoggingService()
