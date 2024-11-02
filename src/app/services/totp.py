from flask import session
from pyotp import random_base32, TOTP

from src.app.services.redis import redis_service


class TOTPService(object):

    def __init__(self, **kwargs):
        self.client_otp = kwargs.get("otp")
        self.client_interval = kwargs.get("interval", 30)
        self.session_key = redis_service.get_session_key("totp")

        self.totp_data = redis_service.db("hgetall", self.session_key)
        self.secret = self.totp_data.get("secret", random_base32())
        self.last_used_otp = self.totp_data.get("last_used_otp", 0)

        self.server_totp = TOTP(self.secret, interval=self.client_interval)
        self.totp_uri = self.server_totp.provisioning_uri(
            name=session["session_id"], issuer_name="open-mfa"
        )

    @property
    def new_data(self):
        return {
            "interval": self.client_interval,
            "secret": self.secret,
            "uri": self.totp_uri,
            "last_used_otp": 0
        }

    def create_totp(self) -> None:
        redis_service.insert_hset(self.session_key, self.new_data)

    def create(self) -> str:
        self.create_totp()
        return self.totp_uri

    def verify(self) -> bool:
        status = self.server_totp.verify(self.client_otp) and self.client_otp != self.last_used_otp
        if status:
            redis_service.db("hset", self.session_key, mapping={"last_used_otp": self.client_otp})
        return status

    def delete(self) -> int:
        if not redis_service.db("exists", self.session_key):
            return 0
        return redis_service.db("delete", self.session_key)
