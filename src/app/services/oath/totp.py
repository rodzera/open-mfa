from pyotp import TOTP
from typing import Dict
from flask import session

from src.app.configs.oath import TOTP_DF_CONFIG
from src.app.utils.helpers.logging import get_logger
from src.app.repositories.oath import TOTPRepository
from src.app.services.oath import BaseOTPService

log = get_logger(__name__)


class TOTPService(BaseOTPService):
    _service_type: str = "totp"
    _df_config: Dict = TOTP_DF_CONFIG
    _repository_class: TOTPRepository = TOTPRepository

    def __init__(self, **client_data):
        super().__init__(self._repository_class, **client_data)

        self._client_interval = client_data.get(
            "interval", self._df_config["min_interval"]
        )
        self._last_used_otp = self._session_data.get("last_used_otp", 0)
        self._valid_window = self._df_config["valid_window"]
        self._server_totp = TOTP(
            self._secret,
            interval=self._client_interval,
            digest=self._hash_method
        )
        self._totp_uri = self._server_totp.provisioning_uri(
            name=session["session_id"],
            issuer_name="open-mfa"
        )

    def _create(self) -> Dict:
        log.debug(f"Starting {self._service_type.upper()} creation")
        self._insert_session_data()
        return {"uri": self._totp_uri}

    def _verify(self) -> Dict:
        log.debug(f"Starting {self._service_type.upper()} verification")
        status = (
            self._server_totp.verify(
                self._client_otp,
                valid_window=self._valid_window
            ) and self._client_otp != self._last_used_otp
        )
        if status:
            self._set_last_used_otp()
        return {"status": status}

    def _set_last_used_otp(self) -> None:
        self._repository.set_last_used_otp(self._client_otp)

    @property
    def _redis_data(self) -> Dict:
        return {
            "interval": self._client_interval,
            "secret": self._b64_cipher_secret,
            "uri": self._totp_uri,
            "last_used_otp": 0
        }
