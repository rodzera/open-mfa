from src.app.infra.redis import redis_service
from src.app.utils.helpers.logging import get_logger
from src.app.services.oath.repositories import BaseOTPRepository

log = get_logger(__name__)


class HOTPRepository(BaseOTPRepository):
    _service_type = "hotp"

    def increase_hotp_counter(self, count: int) -> None:
        log.debug(f"Increasing HOTP counter for session: {self._session_key}")
        redis_service.db(
            "hset", self._session_key, mapping={"count": count + 1}
        )
