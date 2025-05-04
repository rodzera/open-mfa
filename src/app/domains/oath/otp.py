from time import time
from hashlib import sha256
from pyotp import OTP as PyOTP
from typing import Callable, Union

from src.app.configs.oath import OTP_DF_CONFIG
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class OTPGenerator:
    hash_method: Callable = sha256

    def __init__(self, raw_secret: str):
        self.raw_secret = raw_secret
        self.server = PyOTP(self.raw_secret, digest=self.hash_method)

    def generate_code(self, moving_factor: int) -> str:
        return self.server.generate_otp(moving_factor)


class OTPEntity:
    def __init__(
        self,
        code: str,
        hash_secret: str,
        used: int,
        timestamp: int
    ):
        self.code = code
        self.hash_secret = hash_secret
        self.used = int(used)
        self.creation_timestamp = int(timestamp)

    def mark_as_used(self) -> None:
        self.used = 1

    @property
    def is_expired(self) -> bool:
        """ checks if OTP creation has surpassed the expiration range """
        return (
            int(time()) -
            self.creation_timestamp >=
            OTP_DF_CONFIG["expires_in"]
        )

    @property
    def is_valid(self) -> bool:
        """ checks if OTP is neither expired nor used """
        return not self.used and not self.is_expired

    @property
    def as_dict(self) -> dict[str, Union[str, int]]:
        return {
            "code": self.code,
            "secret": self.hash_secret,
            "used": self.used,
            "creation_timestamp": self.creation_timestamp
        }
