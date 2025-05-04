from typing import Dict

from src.app.repositories.redis import RedisRepository


class HealthCheckRepository(RedisRepository):

    def get_current_timestamp(self):
        return self.redis.current_timestamp

    def get_db_version(self) -> Dict:
        return self.redis.info.get("redis_version", "unknown")
