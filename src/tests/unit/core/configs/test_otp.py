from src.core.configs.otp import OTPConfig


def test_otp_config():
    assert OTPConfig.expires_in == 300
