from typing import Union


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
