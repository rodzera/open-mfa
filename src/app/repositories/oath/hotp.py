from src.app.utils.helpers.logging import get_logger
from src.app.repositories.oath import BaseOTPRepository

log = get_logger(__name__)


class HOTPRepository(BaseOTPRepository):
    _service_type = "hotp"

    def increase_hotp_counter(self, count: int) -> None:
        log.debug(f"Increasing HOTP counter for session: {self._oath_session_key}")
        self.redis.db(
            "hset", self._oath_session_key, mapping={"count": count + 1}
        )
