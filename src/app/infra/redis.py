from os import environ
from typing import Union, Dict
from time import strftime, gmtime
from fakeredis import FakeStrictRedis
from redis import StrictRedis, RedisError

from src.app.infra.signals import terminate_server
from src.app.utils.helpers.logging import get_logger
from src.app.infra.exceptions import RedisUnavailableError
from src.app.configs.constants import TESTING_ENV, PRODUCTION_ENV

log = get_logger("redis")


class RedisInfra:
    """
    Redis infrastructure layer.
    """
    def __init__(self):
        if not TESTING_ENV:
            self.client = self.setup_connection()
        else:
            self.client = FakeStrictRedis(decode_responses=True)
        self.debug = PRODUCTION_ENV is False

    @staticmethod
    def setup_connection():
        log.debug("Setting up redis connection")
        # TODO : SSL connection for redis
        return StrictRedis(
            host=environ["_REDIS_HOST"],
            port="6379",
            password=environ["_REDIS_PASS"],
            db=0,
            socket_timeout=3,
            decode_responses=True
        )

    def test_connection(self):
        try:
            log.debug("Testing redis connection")
            self.client.ping()
        except RedisError:
            log.exception("Exception while connecting to Redis")
            terminate_server()

    def db(self, method: str, *args, **kwargs):
        if self.debug:
            log.debug(f"Executing '{method}' with args: {args}, kwargs: {kwargs}")
        return self.execute(method, *args, **kwargs)

    def execute(self, method: str, *args, **kwargs):
        try:
            return getattr(self.client, method)(*args, **kwargs)
        except Exception as e:
            log.error(f"Exception while executing redis: {e}")
            raise RedisUnavailableError() from e

    @property
    def info(self) -> Dict:
        log.debug("Getting redis client info")
        try:
            return self.client.info()
        except RedisError:
            log.exception("Exception while getting redis client info")
            return {}

    @property
    def current_timestamp(self) -> Union[str, bool]:
        log.debug("Querying redis current timestamp")
        try:
            redis_time = self.client.time()
            return strftime("%Y-%m-%d %H:%M:%S", gmtime(redis_time[0]))
        except Exception as e:
            log.error(f"Error fetching redis current timestamp: {e}")
            return False


redis_infra = RedisInfra()
