from dataclasses import dataclass


@dataclass(frozen=True)
class HOTPConfig:
    initial_count: int = 0
    min_resync_threshold: int = 5
    max_resync_threshold: int = 10
