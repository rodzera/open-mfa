from src.app.utils.helpers.logging import get_logger
from src.app.repositories.oath import BaseOTPRepository

log = get_logger(__name__)


class OTPRepository(BaseOTPRepository):
    _service_type = "otp"

    def set_otp_as_used(self) -> None:
        log.debug(f"Setting OTP as used for session: {self._oath_session_key}")
        self.redis.db("hset", self._oath_session_key, mapping={"used": 1})
