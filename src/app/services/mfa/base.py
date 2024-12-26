from hashlib import sha256
from pyotp import random_base32
from typing import Dict, Callable
from base64 import b64encode, b64decode

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service
from src.app.services.aes_cipher import aes_cipher_service

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
    _hash_method: Callable = sha256

    def __init__(self, **kwargs):
        self._client_otp = kwargs.get("otp")
        self._session_key = self._get_session_key()
        self._service_data = redis_service.db("hgetall", self._session_key)
        self._setup_secrets()

    def _setup_secrets(self) -> None:
        if self._service_data:
            self._b64_cipher_secret = self._service_data["secret"]
            self._cipher_secret = b64decode(self._b64_cipher_secret.encode())
            self._secret = aes_cipher_service.decrypt(self._cipher_secret).decode()
        else:
            self._secret = random_base32()
            self._cipher_secret = aes_cipher_service.encrypt(self._secret.encode())
            self._b64_cipher_secret = b64encode(self._cipher_secret).decode()

    def _log_action(self, action: str) -> None:
        log.debug(f"{action.capitalize()} {self._service_type.upper()} for session: {self._session_key}")

    def _create_data(self) -> None:
        redis_service.insert_hset(self._session_key, self._redis_data)

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
