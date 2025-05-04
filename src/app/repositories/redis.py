from src.app.infra.redis import redis_service


class RedisRepository:
    def __init__(self):
        self.redis = redis_service
