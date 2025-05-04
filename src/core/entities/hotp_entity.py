from typing import Union


class HOTPEntity:
    def __init__(
        self,
        hash_secret: str,
        count: int,
        resync_threshold: int
    ):
        self.count = int(count)
        self.hash_secret = hash_secret
        self.resync_threshold = int(resync_threshold)

    def increment(self, amount: int = 1):
        self.count += amount

    @property
    def as_dict(self) -> dict[str, Union[str, int]]:
        return {
            "secret": self.hash_secret,
            "count": self.count,
            "resync_threshold": self.resync_threshold
        }
