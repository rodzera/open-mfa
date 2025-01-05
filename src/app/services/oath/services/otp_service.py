from time import time
from pyotp import OTP
from typing import Dict

from src.app.configs.oath import OTP_DF_CONFIG
from src.app.utils.helpers.logs import get_logger
from src.app.services.oath.repositories import OTPRepository
from src.app.services.oath.services.base_service import BaseOTPService

log = get_logger(__name__)


class OTPService(BaseOTPService):
    _service_type: str = "otp"
    _df_config: Dict = OTP_DF_CONFIG
    _repository_class: OTPRepository = OTPRepository

    def __init__(self, **client_data):
        super().__init__(self._repository_class, **client_data)

        self._cached_otp = self._session_data.get("otp")
        self._used_otp = int(self._session_data.get("used", 0))
        self._current_timestamp = int(time())
        self._creation_timestamp = int(self._session_data.get("timestamp", 0))
        self._server_otp = OTP(
            self._secret,
            digest=self._hash_method
        ).generate_otp(self._current_timestamp)

    def _create(self) -> Dict:
        log.debug(f"Starting {self._service_type.upper()} creation")
        if self._cached_otp and self._is_otp_valid():
            otp = self._cached_otp
        else:
            self._create_session_data()
            otp = self._server_otp
        return {"otp": otp}

    def _verify(self) -> Dict:
        status = (self._client_otp == self._cached_otp) and self._is_otp_valid()
        if status:
            self._set_otp_as_used()
        return {"status": status}

    def _otp_has_expired(self) -> bool:
        """ checks if OTP creation has surpassed the expiration range """
        return (
            self._current_timestamp -
            self._creation_timestamp >=
            self._df_config["expires_in"]
        )

    def _is_otp_valid(self) -> bool:
        """ checks if OTP is neither expired nor used """
        return not self._used_otp and not self._otp_has_expired()

    def _set_otp_as_used(self) -> None:
        self._repository.set_otp_as_used()

    @property
    def _redis_data(self) -> Dict:
        return {
            "otp": self._server_otp,
            "secret": self._b64_cipher_secret,
            "used": 0,
            "timestamp": self._current_timestamp
        }
