from hashlib import sha256
from pyotp import TOTP as PyTOTP
from typing import Union, Callable

from src.app.utils.helpers.logging import get_logger
from src.app.configs.oath import OATH_DF_CONFIG, TOTP_DF_CONFIG

log = get_logger(__name__)

class TOTPGenerator:
    hash_method: Callable = sha256

    def __init__(self, raw_secret: str, interval: int):
        self.server = PyTOTP(
            raw_secret,
            interval=interval,
            digest=self.hash_method
        )

    def generate_uri(self, session_id: str) -> str:
        return self.server.provisioning_uri(
            name=session_id,
            issuer_name=OATH_DF_CONFIG["issuer"]
        )

    def verify(self, code: str) -> bool:
        return self.server.verify(
            code, valid_window=TOTP_DF_CONFIG["valid_window"]
        )


class TOTPEntity:
    def __init__(
        self,
        hash_secret: str,
        interval: int,
        last_used_otp: str = 0
    ):
        self.interval = int(interval)
        self.hash_secret = hash_secret
        self.last_used_otp = last_used_otp


    def is_replay(self, code: str) -> bool:
        return code == self.last_used_otp

    def accept_otp(self, code: str) -> None:
        self.last_used_otp = code

    @property
    def as_dict(self) -> dict[str, Union[str, int]]:
        return {
            "secret": self.hash_secret,
            "interval": self.interval,
            "last_used_otp": self.last_used_otp
        }
