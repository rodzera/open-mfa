from os import environ
from redis import StrictRedis
from logging import getLogger

log = getLogger(__name__)


def redis_check() -> int:
    try:
        client = StrictRedis(
            host=environ["_REDIS_HOST"],
            port="6379",
            password=environ["_REDIS_PASS"],
            db=0,
            socket_timeout=5,
            decode_responses=True
        )
        if client.ping():
            log.debug("Redis connection established")
            return 1
    except RuntimeError as e:
        log.error(f"Error connecting to redis: {e}")
    except KeyError as e:
        log.error(f"Missing env variable: {e}")
        raise KeyError(f"Missing env variable: {e}")
    return 0
