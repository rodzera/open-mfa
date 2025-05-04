from hashlib import sha256

from src.app.configs.oath import OATH_CONFIG, OATHConfig


def test_is_cls():
    assert isinstance(OATH_CONFIG, OATHConfig)

def test_otp_config():
    assert OATH_CONFIG.otp.expires_in == 300

def test_totp_config():
    assert OATH_CONFIG.totp.valid_window == 1
    assert OATH_CONFIG.totp.min_interval == 30
    assert OATH_CONFIG.totp.max_interval == 60

def test_hotp_config():
    assert OATH_CONFIG.hotp.initial_count == 0
    assert OATH_CONFIG.hotp.min_resync_threshold == 5
    assert OATH_CONFIG.hotp.max_resync_threshold == 10

def test_oath_config():
    assert OATH_CONFIG.hash_method == sha256
    assert OATH_CONFIG.issuer == "open-mfa"
