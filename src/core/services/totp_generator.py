from pyotp import TOTP as PyTOTP
from src.app.configs.oath import OATH_CONFIG


class TOTPGenerator:
    def __init__(self, raw_secret: str, interval: int):
        self.server = PyTOTP(
            raw_secret,
            interval=interval,
            digest=OATH_CONFIG.hash_method
        )

    def generate_uri(self, session_id: str) -> str:
        return self.server.provisioning_uri(
            name=session_id,
            issuer_name=OATH_CONFIG.issuer
        )

    def verify(self, code: str) -> bool:
        return self.server.verify(
            code, valid_window=OATH_CONFIG.totp.valid_window
        )
