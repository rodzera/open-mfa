from typing import Optional
from datetime import timedelta

from src.app.configs.types import OTPType
from src.app.utils.helpers.logging import get_logger
from src.app.repositories.redis import RedisRepository
from src.app.services.user_session import UserSessionService

log = get_logger(__name__)


class OTPRepository(RedisRepository):
    """
    Base data layer class for OTP repositories.
    """
    oath_session_key: str
    service_type: OTPType
    user_session = UserSessionService

    def __init__(self, service_type: OTPType):
        super().__init__()
        self.service_type = service_type

    def log_action(self, action: str) -> None:
        log.debug(
            f"{action.capitalize()} {self.service_type.upper()} "
            f"for session: {self.oath_session_key}"
        )

    def get_session_data(self) -> Optional[dict]:
        return self.redis.db("hgetall", self.oath_session_key)

    def insert_session_data(self, data: dict, exp: bool = False) -> None:
        self.redis.db("hset", self.oath_session_key, mapping=data)
        if exp:
            self.redis.db("expire", self.oath_session_key, timedelta(minutes=60))

    def check_session_data_exists(self) -> int:
        return self.redis.db("exists", self.oath_session_key)

    def delete_session_data(self) -> int:
        return self.redis.db("delete", self.oath_session_key)

    def get_oath_session_key(self, method: OTPType) -> str:
        session_id = self.user_session().manage_session()
        return f"{session_id}:{method}"

    @property
    def oath_session_key(self) -> str:
        return self.get_oath_session_key(self.service_type)

    @property
    def user_session_id(self) -> str:
        return self.user_session().manage_session()
