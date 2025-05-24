from dataclasses import dataclass


@dataclass(frozen=True)
class OTPConfig:
    expires_in: int = 300
