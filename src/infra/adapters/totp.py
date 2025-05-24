from pyotp import TOTP as PyTOTP
from src.core.configs.base import OATH_CONFIG
from src.core.ports.totp import TOTPGeneratorPort
from src.infra.adapters.shared import default_hash_method


class TOTPGenerator(TOTPGeneratorPort):
    def __init__(self, raw_secret: str, interval: int):
        self.server = PyTOTP(
            raw_secret,
            interval=interval,
            digest=default_hash_method
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
