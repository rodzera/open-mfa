from src.core.configs.hotp import HOTPConfig


def test_hotp_config():
    assert HOTPConfig.initial_count == 0
    assert HOTPConfig.min_resync_threshold == 5
    assert HOTPConfig.max_resync_threshold == 10
