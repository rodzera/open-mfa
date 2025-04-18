OATH_DF_CONFIG = {
    "otp": {
      "expires_in": 300
    },
    "totp": {
        "valid_window": 1,
        "min_interval": 30,
        "max_interval": 60
    },
    "hotp": {
        "initial_count": 0,
        "min_resync_threshold": 5,
        "max_resync_threshold": 10
    }
}

OTP_DF_CONFIG = OATH_DF_CONFIG["otp"]
TOTP_DF_CONFIG = OATH_DF_CONFIG["totp"]
HOTP_DF_CONFIG = OATH_DF_CONFIG["hotp"]
