from os import environ
from flask import session
from redis import StrictRedis
from datetime import timedelta
from time import strftime, gmtime
from typing import Union, Literal, Dict

from src.app.configs.constants import TESTING_ENV
from src.app.utils.helpers.logs import get_logger

log = get_logger("redis")


class RedisService(object):
    def __init__(self):
        if not TESTING_ENV:
            self.client = self.setup_connection()
        else:
            self.client = None

    def db(self, method: str, *args, **kwargs):
        log.debug(
            f"Executing Redis command: {method}, args: {args}, kwargs: {kwargs}"
        )
        return getattr(self.client, method)(*args, **kwargs)

    @staticmethod
    def insert_hset(
        session_key: str, hset: Dict[str, str], exp: int = 60
    ) -> None:
        log.debug(f"Inserting hset key: {hset}")
        redis_service.db("hset", session_key, mapping=hset)
        redis_service.db("expire", session_key, timedelta(minutes=exp))

    @staticmethod
    def setup_connection():
        log.debug("Setting up redis connection")
        client = StrictRedis(
            host=environ["_REDIS_HOST"],
            port="6379",
            password=environ["_REDIS_PASS"],
            db=0,
            socket_timeout=5,
            decode_responses=True
        )
        return client if client.ping() else None

    @property
    def info(self):
        log.debug("Getting redis client info")
        return self.client.info()

    @property
    def current_timestamp(self) -> Union[str, bool]:
        log.debug("Querying redis current timestamp")
        try:
            redis_time = self.client.time()
            return strftime('%Y-%m-%d %H:%M:%S', gmtime(redis_time[0]))
        except Exception as e:
            log.error(f"Error fetching redis current timestamp: {e}")
            return False

    @staticmethod
    def get_session_key(method: Literal["otp", "totp", "hotp"]) -> str:
        session_id = session["session_id"]
        return f"{session_id}:{method}"


redis_service = RedisService()
