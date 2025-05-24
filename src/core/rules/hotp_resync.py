from src.core.ports.hotp import HOTPGeneratorPort
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class HOTPResyncService:
    def __init__(self, generator: HOTPGeneratorPort):
        self.generator = generator

    def resync(self, code: str, threshold: int) -> tuple[bool, int]:
        """
        Look-ahead window resynchronization protocol:
        https://datatracker.ietf.org/doc/html/rfc4226#page-11
        """
        log.debug("Triggering resync protocol")
        for n in range(threshold):
            lookahead_counter = n + 1
            if self.generator.verify(code, lookahead_counter):
                log.debug("Resync protocol successful")
                return True, lookahead_counter
        return False, 0
