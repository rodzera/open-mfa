from datetime import timedelta
from typing import Dict, Literal, Optional

from src.app.repositories.base_repository import BaseRepository
from src.app.utils.helpers.logging import get_logger
from src.app.controllers.user_session import UserSessionController

log = get_logger(__name__)


class BaseOTPRepository(BaseRepository):
    """
    Base data layer class for OTP repositories.
    """
    _oath_session_key: str
    _user_session = UserSessionController
    _service_type: Literal["otp", "totp", "hotp"]

    def _log_action(self, action: str) -> None:
        log.debug(f"{action.capitalize()} {self._service_type.upper()} for session: {self._oath_session_key}")

    def get_session_data(self) -> Optional[Dict]:
        return self.redis.db("hgetall", self._oath_session_key)

    def insert_session_data(self, redis_data: Dict) -> None:
        self.redis.db("hset", self._oath_session_key, mapping=redis_data)
        self.redis.db("expire", self._oath_session_key, timedelta(minutes=60))

    def check_session_data_exists(self) -> int:
        return self.redis.db("exists", self._oath_session_key)

    def delete_session_data(self) -> int:
        return self.redis.db("delete", self._oath_session_key)

    def get_oath_session_key(self, method: Literal["otp", "totp", "hotp"]) -> str:
        session_id = self._user_session.manage_session()
        # TODO : oath key must be build by another layer
        return f"{session_id}:{method}"

    @property
    def _oath_session_key(self) -> str:
        return self.get_oath_session_key(self._service_type)
