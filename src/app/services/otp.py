from time import time
from datetime import timedelta
from pyotp import random_base32, OTP

from src.app.services.redis import redis_service


class OTPService(object):

    def __init__(self, **kwargs):
        self.client_otp = kwargs.get("otp")

        self.current_time = self.get_current_time()
        self.session_key = redis_service.get_session_key("otp")

        self.otp_data = redis_service.db("hgetall", self.session_key)
        self.secret = self.otp_data.get("secret", random_base32())
        self.cached_otp = self.otp_data.get("otp")
        self.cached_timestamp = int(self.otp_data.get("timestamp", 0))
        self.cached_exp = int(self.otp_data.get("exp", 0))

        self.server_otp = OTP(self.secret).generate_otp(self.current_time)

    def create_flow(self) -> str:
        if self.cached_otp and (self.cached_timestamp == self.current_time):
            return self.cached_otp
        else:
            self.insert_otp_into_redis()
            return self.server_otp

    def insert_otp_into_redis(self) -> None:
        redis_service.db(
            "hset", self.session_key, mapping={
                "otp": self.server_otp,
                "secret": self.secret,
                "exp": 0,
                "timestamp": self.current_time
            }
        )
        redis_service.db(
            "expire", self.session_key, timedelta(minutes=5)  # after five minutes a used or not otp will be removed
        )

    def verify_flow(self) -> bool:
        status = (self.server_otp == self.client_otp == self.cached_otp) and not self.cached_exp
        if status:
            redis_service.db("hset", self.session_key, mapping={"exp": 1})
        return status

    @staticmethod
    def get_current_time() -> int:
        return int(time()) // 300 # OTP will be valid for five minutes
