from pyotp import HOTP as PyHOTP
from src.app.configs.oath import OATH_CONFIG
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class HOTPGenerator:
    def __init__(
        self,
        raw_secret: str,
        initial_count: int
    ):
        self.server = PyHOTP(
            raw_secret,
            digest=OATH_CONFIG.hash_method,
            initial_count=initial_count
        )

    def generate_uri(self, session_id: str) -> str:
        return self.server.provisioning_uri(
            name=session_id,
            issuer_name=OATH_CONFIG.issuer
        )

    def verify(self, code: str, moving_factor: int = 0) -> bool:
        return self.server.verify(code, moving_factor)

    def resync_protocol(
        self,
        code: str,
        threshold: int
    ) -> tuple[bool, int]:
        """
        Look-ahead window resynchronization protocol:
        https://datatracker.ietf.org/doc/html/rfc4226#page-11
        """

        log.debug("Triggering resync protocol")
        for n in range(threshold):
            lookahead_counter = 0 + n + 1
            if self.verify(code, lookahead_counter):
                log.debug("Resync protocol successful")
                return True, lookahead_counter
        return False, 0
