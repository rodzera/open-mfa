from typing import Dict, Literal

from src.app.services.redis import redis_service
from src.app.utils.helpers.logs import get_logger

log = get_logger(__name__)


class BaseOTPRepository:
    """
    Base repository class for OTP services.
    """
    _session_key: str
    _service_type: Literal["otp", "totp", "hotp"]

    def _log_action(self, action: str) -> None:
        log.debug(f"{action.capitalize()} {self._service_type.upper()} for session: {self._session_key}")

    def get_server_data(self):
        return redis_service.db("hgetall", self._session_key)

    def create_server_data(self, redis_data: Dict) -> None:
        redis_service.insert_hset(self._session_key, redis_data)

    def verify_session_key_exists(self) -> int:
        return redis_service.db("exists", self._session_key)

    def delete_session_key(self) -> int:
        return redis_service.db("delete", self._session_key)

    @property
    def _session_key(self) -> str:
        return redis_service.get_session_key(self._service_type)


class OTPRepository(BaseOTPRepository):
    _service_type = "otp"

    def set_otp_as_used(self) -> None:
        log.debug(f"Setting OTP as used for session: {self._session_key}")
        redis_service.db("hset", self._session_key, mapping={"used": 1})


class TOTPRepository(BaseOTPRepository):
    _service_type = "totp"

    def set_last_used_otp(self, client_otp: str) -> None:
        log.debug(f"Setting last used OTP for session: {self._session_key}")
        redis_service.db(
            "hset", self._session_key, mapping={"last_used_otp": client_otp}
        )


class HOTPRepository(BaseOTPRepository):
    _service_type = "hotp"

    def increase_hotp_counter(self, count: int) -> None:
        log.debug(f"Increasing HOTP counter for session: {self._session_key}")
        redis_service.db(
            "hset", self._session_key, mapping={"count": count + 1}
        )
