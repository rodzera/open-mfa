from src.app.infra.redis import redis_infra


class RedisRepository:
    def __init__(self):
        self.redis = redis_infra
