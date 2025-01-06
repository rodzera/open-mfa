from typing import Optional

from src.app.repositories.base_repository import BaseRepository


class LoggingRepository(BaseRepository):

    def get_app_logging_level(self) -> Optional[str]:
        return self.redis.db("get", "log")

    def set_app_logging_level(self, level: int) -> bool:
        return self.redis.db("set", "log", level)
