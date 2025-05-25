from dataclasses import dataclass


@dataclass(frozen=True)
class TOTPConfig:
    valid_window: int = 1
    min_interval: int = 30
    max_interval: int = 60
