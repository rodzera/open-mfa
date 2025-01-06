from src.app.utils.helpers.logging import get_logger
from src.app.repositories.oath import BaseOTPRepository

log = get_logger(__name__)


class TOTPRepository(BaseOTPRepository):
    _service_type = "totp"

    def set_last_used_otp(self, client_otp: str) -> None:
        log.debug(f"Setting last used OTP for session: {self._oath_session_key}")
        self.redis.db(
            "hset", self._oath_session_key, mapping={"last_used_otp": client_otp}
        )
