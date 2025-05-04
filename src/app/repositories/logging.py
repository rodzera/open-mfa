from typing import Optional

from src.app.repositories.redis import RedisRepository


class LoggingRepository(RedisRepository):

    def get_level(self) -> Optional[str]:
        return self.redis.db("get", "log")

    def set_level(self, level: int) -> bool:
        return self.redis.db("set", "log", level)
