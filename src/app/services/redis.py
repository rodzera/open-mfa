from os import environ
from flask import session
from datetime import timedelta
from time import strftime, gmtime
from typing import Union, Literal, Dict
from redis import RedisError, StrictRedis

from src.app.logger import get_logger

log = get_logger("redis")


class RedisService(object):
    def __init__(self):
        self.client = self.setup_connection()

    def db(self, method: str, *args, **kwargs):
        log.debug(
            f"Executing Redis command: {method}, args: {args}, kwargs: {kwargs}"
        )
        return getattr(self.client, method)(*args, **kwargs)

    @staticmethod
    def insert_hset(
        session_key: str, hset: Dict[str, str], exp: int = 60
    ) -> None:
        redis_service.db("hset", session_key, mapping=hset)
        redis_service.db("expire", session_key, timedelta(minutes=exp))

    @staticmethod
    def setup_connection():
        try:
            client = StrictRedis(
                host=environ["_REDIS_HOST"],
                port="6379",
                password=environ["_REDIS_PASS"],
                db=0,
                socket_timeout=5,
                decode_responses=True
            )
            return client if client.ping() else None
        except RedisError as e:
            log.exception("Redis connection failed:")
            raise e

    @property
    def info(self):
        return self.client.info()

    @property
    def current_timestamp(self) -> Union[str, bool]:
        log.info("Querying redis current timestamp")
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
