from typing import Dict
from pyotp import random_base32

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service

log = get_logger(__name__)


class RedisOTPHelperService(object):
    """
    Redis helper class for OTP services.
    """
    def _get_session_key(self) -> str:
        return redis_service.get_session_key(self._service_type)

    def _verify_session_key_exists(self) -> int:
        return redis_service.db("exists", self._session_key)

    def _delete_session_key(self) -> int:
        return redis_service.db("delete", self._session_key)


class BaseOTPService(RedisOTPHelperService):
    """
    Base class for OTP Services (OTP, TOTP, HOTP)
    """
    _secret: str
    _service_data: Dict
    _service_type: str
    _session_key: str = None

    def __init__(self, **kwargs):
        self._client_otp = kwargs.get("otp")
        self._session_key = self._get_session_key()
        self._service_data = redis_service.db("hgetall", self._session_key)
        self._secret = self._service_data.get("secret", random_base32())

    def _log_action(self, action: str) -> None:
        log.debug(f"{action.capitalize()} {self._service_type.upper()} for session: {self._session_key}")

    def _create_data(self) -> None:
        redis_service.insert_hset(self._session_key, self._default_data)

    def delete_data(self) -> int:
        if self._service_type == "otp":
            raise AttributeError("Delete method is not available for OTP service")

        self._log_action("delete")
        if not self._verify_session_key_exists():
            return 0
        return self._delete_session_key()

    def process_request(self) -> Dict:
        if self._client_otp:
            return self._verify()
        else:
            return self._create()
