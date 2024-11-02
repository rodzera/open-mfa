from time import time
from pyotp import random_base32, OTP

from src.app.services.redis import redis_service


class OTPService(object):

    def __init__(self, **kwargs):
        self.client_otp = kwargs.get("otp")
        self.current_timestamp = int(time())
        self.session_key = redis_service.get_session_key("otp")

        self.otp_data = redis_service.db("hgetall", self.session_key)
        self.secret = self.otp_data.get("secret", random_base32())
        self.cached_otp = self.otp_data.get("otp")
        self.creation_timestamp = int(self.otp_data.get("timestamp", 0))
        self.used_otp = int(self.otp_data.get("used", 0))

        self.server_otp = OTP(self.secret).generate_otp(self.current_timestamp)

    @property
    def new_data(self):
        return {
            "otp": self.server_otp,
            "secret": self.secret,
            "used": 0,
            "timestamp": self.current_timestamp
        }

    def create_otp(self) -> None:
        redis_service.insert_hset(self.session_key, self.new_data)

    def otp_has_expired(self):
        return self.current_timestamp - self.creation_timestamp >= 300  # five minutes expiration

    def create(self) -> str:
        if self.cached_otp and not self.used_otp and not self.otp_has_expired():
            return self.cached_otp
        else:
            self.create_otp()
            return self.server_otp

    def verify(self) -> bool:
        status = (self.client_otp == self.cached_otp) and not self.used_otp and not self.otp_has_expired()
        if status:
            redis_service.db("hset", self.session_key, mapping={"used": 1})
        return status
