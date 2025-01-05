from src.app.services.oath.default_config import OATH_DF_CONFIG

def test_is_a_dict():
    assert isinstance(OATH_DF_CONFIG, dict)

def test_otp_config():
    data = OATH_DF_CONFIG["otp"]
    assert data["expires_in"] == 300

def test_totp_config():
    data = OATH_DF_CONFIG["totp"]
    assert data["interval"] == 30
    assert data["valid_window"] == 1

def test_hotp_config():
    data = OATH_DF_CONFIG["hotp"]
    assert data["initial_count"] == 0
    assert data["min_resync_threshold"] == 5
    assert data["max_resync_threshold"] == 10
