from dataclasses import dataclass
from hashlib import sha256
from typing import Callable


@dataclass(frozen=True)
class OTPConfig:
    expires_in: int = 300


@dataclass(frozen=True)
class TOTPConfig:
    valid_window: int = 1
    min_interval: int = 30
    max_interval: int = 60


@dataclass(frozen=True)
class HOTPConfig:
    initial_count: int = 0
    min_resync_threshold: int = 5
    max_resync_threshold: int = 10


@dataclass(frozen=True)
class OATHConfig:
    """
    Default OATH configuration.
    """
    otp: OTPConfig
    totp: TOTPConfig
    hotp: HOTPConfig
    issuer: str = "open-mfa"
    hash_method: Callable = sha256


OATH_CONFIG = OATHConfig(
    hash_method=sha256,
    issuer="open-mfa",
    otp=OTPConfig(),
    totp=TOTPConfig(),
    hotp=HOTPConfig()
)
