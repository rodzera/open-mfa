from dataclasses import dataclass

from src.core.configs.otp import OTPConfig
from src.core.configs.hotp import HOTPConfig
from src.core.configs.totp import TOTPConfig


@dataclass(frozen=True)
class OATHConfig:
    """
    Default OATH configuration.
    """
    otp: OTPConfig
    totp: TOTPConfig
    hotp: HOTPConfig
    issuer: str = "open-mfa"


OATH_CONFIG = OATHConfig(
    otp=OTPConfig(),
    totp=TOTPConfig(),
    hotp=HOTPConfig()
)
