from src.app.infra.redis import redis_service


class BaseRepository:
    def __init__(self):
        self.redis = redis_service
