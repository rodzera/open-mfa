from src.core.configs.totp import TOTPConfig


def test_totp_config():
    assert TOTPConfig.valid_window == 1
    assert TOTPConfig.min_interval == 30
    assert TOTPConfig.max_interval == 60
