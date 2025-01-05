from typing import Dict, Literal

from src.app.infra.redis import redis_service
from src.app.utils.helpers.logs import get_logger

log = get_logger(__name__)


class BaseOTPRepository:
    """
    Base data layer class for OTP repositories.
    """
    _session_key: str
    _service_type: Literal["otp", "totp", "hotp"]

    def _log_action(self, action: str) -> None:
        log.debug(f"{action.capitalize()} {self._service_type.upper()} for session: {self._session_key}")

    def get_session_data(self):
        return redis_service.db("hgetall", self._session_key)

    def insert_session_data(self, redis_data: Dict) -> None:
        redis_service.insert_hset(self._session_key, redis_data)

    def check_session_data_exists(self) -> int:
        return redis_service.db("exists", self._session_key)

    def delete_session_data(self) -> int:
        return redis_service.db("delete", self._session_key)

    @property
    def _session_key(self) -> str:
        return redis_service.get_session_key(self._service_type)
