from src.core.configs.otp import OTPConfig
from src.core.configs.hotp import HOTPConfig
from src.core.configs.totp import TOTPConfig
from src.core.configs.base import OATH_CONFIG, OATHConfig


def test_is_cls():
    assert isinstance(OATH_CONFIG, OATHConfig)


def test_oath_config():
    assert OATH_CONFIG.issuer == "open-mfa"
    assert isinstance(OATH_CONFIG.otp, OTPConfig)
    assert isinstance(OATH_CONFIG.hotp, HOTPConfig)
    assert isinstance(OATH_CONFIG.totp, TOTPConfig)
