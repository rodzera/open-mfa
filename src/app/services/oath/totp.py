from pyotp import TOTP
from typing import Dict
from flask import session

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service
from src.app.services.oath.base import BaseOTPService

log = get_logger(__name__)


class TOTPService(BaseOTPService):
    _service_type = "totp"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client_interval = kwargs.get("interval", 30)
        self._last_used_otp = self._service_data.get("last_used_otp", 0)
        self._server_totp = TOTP(
            self._secret, interval=self._client_interval,
            digest=self._hash_method
        )
        self._totp_uri = self._server_totp.provisioning_uri(
            name=session["session_id"], issuer_name="open-mfa"
        )

    def _create(self) -> Dict:
        self._log_action("create")
        self._create_data()
        return {"uri": self._totp_uri}

    def _verify(self) -> Dict:
        self._log_action("verify")
        status = self._server_totp.verify(self._client_otp) and self._client_otp != self._last_used_otp
        if status:
            self._set_last_used_otp()
        return {"status": status}

    @property
    def _redis_data(self) -> Dict:
        return {
            "interval": self._client_interval,
            "secret": self._b64_cipher_secret,
            "uri": self._totp_uri,
            "last_used_otp": 0
        }

    def _set_last_used_otp(self) -> None:
        redis_service.db(
            "hset", self._session_key,
            mapping={"last_used_otp": self._client_otp}
        )
