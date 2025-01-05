from src.app.infra.redis import redis_service


class HealthCheckRepository:

    @staticmethod
    def get_db_version():
        return redis_service.info.get("redis_version", "unknown")
