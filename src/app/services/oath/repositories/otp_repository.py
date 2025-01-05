from src.app.infra.redis import redis_service
from src.app.utils.helpers.logging import get_logger
from src.app.services.oath.repositories import BaseOTPRepository

log = get_logger(__name__)


class OTPRepository(BaseOTPRepository):
    _service_type = "otp"

    def set_otp_as_used(self) -> None:
        log.debug(f"Setting OTP as used for session: {self._session_key}")
        redis_service.db("hset", self._session_key, mapping={"used": 1})
