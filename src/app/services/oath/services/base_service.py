from hashlib import sha256
from pyotp import random_base32
from abc import ABC, abstractmethod
from base64 import b64encode, b64decode
from typing import Dict, Callable, Union, Literal

from src.app.utils.helpers.logs import get_logger
from src.app.infra.aes_cipher import aes_cipher_service
from src.app.services.oath.repositories import OTPRepository, TOTPRepository, \
    HOTPRepository

log = get_logger(__name__)


class BaseOTPService(ABC):
    """
    Base service layer class for OTP services.
    """
    _secret: str
    _session_data: Dict
    _hash_method: Callable = sha256
    _service_type: Literal["otp", "totp", "hotp"]
    _repository: Union[OTPRepository, TOTPRepository, HOTPRepository]

    def __init__(self, repository, **kwargs):
        self._repository = repository()
        self._client_otp = kwargs.get("otp")
        self._session_data = self._get_session_data()
        self._setup_secrets()

    def _get_session_data(self):
        return self._repository.get_session_data()

    def _create_session_data(self) -> None:
        self._repository.create_session_data(self._redis_data)

    def _verify_session_key_exists(self) -> int:
        return self._repository.verify_session_key_exists()

    def _delete_session_key(self) -> int:
        return self._repository.delete_session_key()

    def _setup_secrets(self) -> None:
        if self._session_data:
            self._b64_cipher_secret = self._session_data["secret"]
            self._cipher_secret = b64decode(self._b64_cipher_secret.encode())
            self._secret = aes_cipher_service.decrypt(self._cipher_secret).decode()
        else:
            self._secret = random_base32()
            self._cipher_secret = aes_cipher_service.encrypt(self._secret.encode())
            self._b64_cipher_secret = b64encode(self._cipher_secret).decode()

    def delete_data(self) -> int:
        log.debug(f"Starting {self._service_type.upper()} deletion")
        if self._service_type == "otp":
            raise AttributeError(
                "Delete method is not available for OTP service"
            )

        if not self._verify_session_key_exists():
            return 0
        return self._delete_session_key()

    def process_request(self) -> Dict:
        if self._client_otp:
            return self._verify()
        else:
            return self._create()

    @property
    @abstractmethod
    def _redis_data(self) -> Dict:
        pass

    @abstractmethod
    def _verify(self):
        pass

    @abstractmethod
    def _create(self):
        pass
