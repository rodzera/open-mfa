from flask import session
from pyotp import random_base32, HOTP

from src.app.services.redis import redis_service


class HOTPService(object):

    def __init__(self, **kwargs):
        self.client_otp = kwargs.get("otp")
        self.client_initial_count = kwargs.get("initial_count", 0)
        self.session_key = redis_service.get_session_key("hotp")

        self.hotp_data = redis_service.db("hgetall", self.session_key)
        self.secret = self.hotp_data.get("secret", random_base32())
        self.cached_count = int(self.hotp_data.get("count", 0))

        self.server_hotp = HOTP(self.secret, initial_count=self.client_initial_count)
        self.hotp_uri = self.server_hotp.provisioning_uri(
            name=session["session_id"], issuer_name="open-mfa",
            initial_count=self.client_initial_count
        )

    @property
    def new_hotp_data(self):
        return {
            "count": self.client_initial_count,
            "secret": self.secret,
            "uri": self.hotp_uri
        }

    def create_hotp(self) -> None:
        redis_service.insert_hset(self.session_key, self.new_hotp_data)

    def create(self) -> str:
        self.create_hotp()
        return self.hotp_uri

    def verify(self) -> bool:
        status = self.server_hotp.verify(self.client_otp, self.cached_count + 1)  # TODO : edge case gg authenticator
        if status:
            redis_service.db("hset", self.session_key, mapping={"count": self.cached_count + 1})
        return status

    def delete(self) -> int:
        if not redis_service.db("exists", self.session_key):
            return 0
        return redis_service.db("delete", self.session_key)
