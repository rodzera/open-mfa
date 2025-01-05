from typing import Optional

from src.app.infra.redis import redis_service


class LoggingRepository:

    @staticmethod
    def get_app_logging_level() -> Optional[str]:
        return redis_service.db("get", "log")

    @staticmethod
    def set_app_logging_level(level: int) -> bool:
        return redis_service.db("set", "log", level)
