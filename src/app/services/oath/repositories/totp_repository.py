from src.app.infra.redis import redis_service
from src.app.utils.helpers.logs import get_logger
from src.app.services.oath.repositories import BaseOTPRepository

log = get_logger(__name__)


class TOTPRepository(BaseOTPRepository):
    _service_type = "totp"

    def set_last_used_otp(self, client_otp: str) -> None:
        log.debug(f"Setting last used OTP for session: {self._session_key}")
        redis_service.db(
            "hset", self._session_key, mapping={"last_used_otp": client_otp}
        )
