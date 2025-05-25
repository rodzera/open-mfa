from time import time
from typing import  Union
from src.core.configs.base import OATH_CONFIG


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
        return (
            int(time()) -
            self.creation_timestamp >=
            OATH_CONFIG.otp.expires_in
        )

    @property
    def is_valid(self) -> bool:
        return not self.used and not self.is_expired

    @property
    def as_dict(self) -> dict[str, Union[str, int]]:
        return {
            "code": self.code,
            "secret": self.hash_secret,
            "used": self.used,
            "creation_timestamp": self.creation_timestamp
        }
