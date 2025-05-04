from pyotp import OTP as PyOTP
from src.app.configs.oath import OATH_CONFIG


class OTPGenerator:
    def __init__(self, raw_secret: str):
        self.raw_secret = raw_secret
        self.server = PyOTP(
            self.raw_secret,
            digest=OATH_CONFIG.hash_method
        )

    def generate_code(self, moving_factor: int) -> str:
        return self.server.generate_otp(moving_factor)
