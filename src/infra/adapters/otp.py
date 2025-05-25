from pyotp import OTP as PyOTP
from src.core.ports.otp import OTPGeneratorPort
from src.infra.adapters.shared import default_hash_method


class OTPGenerator(OTPGeneratorPort):
    def __init__(self, raw_secret: str):
        self.server = PyOTP(
            raw_secret,
            digest=default_hash_method
        )

    def generate_code(self, moving_factor: int) -> str:
        return self.server.generate_otp(moving_factor)
