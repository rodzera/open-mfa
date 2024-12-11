from logging import getLogger

from app.services.redis import redis_service

log = getLogger(__name__)


def redis_check() -> int:
    try:
        if redis_service.setup_connection():
            log.debug("Redis connection established")
            return 1
    except RuntimeError as e:
        log.error(f"Error connecting to redis: {e}")
    except KeyError as e:
        log.error(f"Missing env variable: {e}")
        raise KeyError(f"Missing env variable: {e}")
    return 0
