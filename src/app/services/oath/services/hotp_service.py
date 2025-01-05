from pyotp import HOTP
from flask import session
from typing import Dict, Tuple

from src.app.configs.oath import HOTP_DF_CONFIG
from src.app.utils.helpers.logging import get_logger
from src.app.services.oath.repositories import HOTPRepository
from src.app.services.oath.services.base_service import BaseOTPService

log = get_logger(__name__)


class HOTPService(BaseOTPService):
    _service_type: str = "hotp"
    _df_config: Dict = HOTP_DF_CONFIG
    _repository_class: HOTPRepository = HOTPRepository

    def __init__(self, **client_data):
        super().__init__(self._repository_class, **client_data)

        self._client_initial_count = client_data.get(
            "initial_count", self._df_config["initial_count"]
        )
        self._client_resync_threshold = client_data.get(
            "resync_threshold", self._df_config["min_resync_threshold"]
        )
        self._cached_count = int(self._session_data.get("count", 0))
        self._resync_threshold = int(
            self._session_data.get(
                "resync_threshold", self._df_config["min_resync_threshold"]
            )
        )
        self._server_hotp = HOTP(
            self._secret,
            digest=self._hash_method,
            initial_count=self._client_initial_count
        )
        self._hotp_uri = self._server_hotp.provisioning_uri(
            name=session["session_id"], issuer_name="open-mfa",
            initial_count=self._client_initial_count
        )

    def _create(self) -> Dict:
        log.debug(f"Starting {self._service_type.upper()} creation")
        self._insert_session_data()
        return {"uri": self._hotp_uri}

    def _verify(self) -> Dict:
        log.debug(f"Starting {self._service_type.upper()} verification")
        counter = self._cached_count
        status = self._server_hotp.verify(self._client_otp, counter)
        if not status:
            status, counter = self._trigger_resync_protocol()
        if status:
            self._increase_hotp_counter(counter)
        return {"status": status}

    def _trigger_resync_protocol(self) -> Tuple[bool, int]:
        """
        Look-ahead window resynchronization protocol:
        https://datatracker.ietf.org/doc/html/rfc4226#page-11
        """
        log.debug("Triggering resync protocol")
        for c in range(0, self._resync_threshold):
            look_ahead_counter = self._cached_count + (c + 1)
            status = self._server_hotp.verify(
                self._client_otp, look_ahead_counter
            )
            if status:
                return status, look_ahead_counter
        return False, 0

    def _increase_hotp_counter(self, count: int) -> None:
        self._repository.increase_hotp_counter(count)

    @property
    def _redis_data(self) -> Dict:
        return {
            "count": self._client_initial_count,
            "secret": self._b64_cipher_secret,
            "uri": self._hotp_uri,
            "resync_threshold": self._client_resync_threshold
        }
