from logging import getLogger
from src.infra.redis import redis_infra

log = getLogger(__name__)


def check_redis_conn() -> int:
    try:
        if redis_infra.client.ping():
            log.info("Redis connection established")
            return 1
    except Exception:
        log.exception("Exception while connecting to Redis")
    return 0
