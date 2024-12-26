from time import time
from pyotp import OTP
from typing import Dict

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service
from src.app.services.mfa.base import BaseOTPService

log = get_logger(__name__)


class OTPService(BaseOTPService):
    _service_type = "otp"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_timestamp = int(time())
        self._cached_otp = self._service_data.get("otp")
        self._creation_timestamp = int(self._service_data.get("timestamp", 0))
        self._used_otp = int(self._service_data.get("used", 0))
        self._server_otp = OTP(self._secret, digest=self._hash_method).generate_otp(self._current_timestamp)

    def _create(self) -> Dict:
        self._log_action("create")
        if self._cached_otp and self._is_otp_valid():
            otp = self._cached_otp
        else:
            self._create_data()
            otp = self._server_otp
        return {"otp": otp}

    def _verify(self) -> Dict:
        self._log_action("verify")
        status = (self._client_otp == self._cached_otp) and self._is_otp_valid()
        if status:
            self._set_otp_as_used()
        return {"status": status}

    @property
    def _redis_data(self) -> Dict:
        return {
            "otp": self._server_otp,
            "secret": self._b64_cipher_secret,
            "used": 0,
            "timestamp": self._current_timestamp
        }

    def _set_otp_as_used(self) -> None:
        redis_service.db("hset", self._session_key, mapping={"used": 1})

    def _otp_has_expired(self) -> bool:
        """ checks if OTP creation has surpassed five minute """
        return self._current_timestamp - self._creation_timestamp >= 300

    def _is_otp_valid(self) -> bool:
        """ checks if OTP is neither expired nor used """
        return not self._used_otp and (self._current_timestamp - self._creation_timestamp < 300)
