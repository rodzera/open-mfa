from pyotp import HOTP as PyHOTP

from src.core.configs.base import OATH_CONFIG
from src.core.ports.hotp import HOTPGeneratorPort
from src.app.utils.helpers.logging import get_logger
from src.infra.adapters.shared import default_hash_method

log = get_logger(__name__)


class HOTPGenerator(HOTPGeneratorPort):
    def __init__(
        self,
        raw_secret: str,
        initial_count: int
    ):
        self.server = PyHOTP(
            raw_secret,
            digest=default_hash_method,
            initial_count=initial_count
        )

    def generate_uri(self, session_id: str) -> str:
        return self.server.provisioning_uri(
            name=session_id,
            issuer_name=OATH_CONFIG.issuer
        )

    def verify(self, code: str, moving_factor: int = 0) -> bool:
        return self.server.verify(code, moving_factor)
