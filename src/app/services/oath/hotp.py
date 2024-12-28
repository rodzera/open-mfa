from pyotp import HOTP
from flask import session
from typing import Dict, Tuple

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service
from src.app.services.oath.base import BaseOTPService

log = get_logger(__name__)


class HOTPService(BaseOTPService):
    _service_type = "hotp"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client_initial_count = kwargs.get("initial_count", 0)
        self._client_resync_threshold = kwargs.get("resync_threshold", 5)
        self._cached_count = int(self._service_data.get("count", 0))
        self._resync_threshold = int(self._service_data.get("resync_threshold", 5))
        self._server_hotp = HOTP(
            self._secret, initial_count=self._client_initial_count,
            digest=self._hash_method
        )
        self._hotp_uri = self._server_hotp.provisioning_uri(
            name=session["session_id"], issuer_name="open-mfa",
            initial_count=self._client_initial_count
        )

    def _create(self) -> Dict:
        self._log_action("create")
        self._create_data()
        return {"uri": self._hotp_uri}

    def _verify(self) -> Dict:
        self._log_action("verify")

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
            status = self._server_hotp.verify(self._client_otp, look_ahead_counter)
            if status:
                return status, look_ahead_counter
        return False, 0

    @property
    def _redis_data(self) -> Dict:
        return {
            "count": self._client_initial_count,
            "secret": self._b64_cipher_secret,
            "uri": self._hotp_uri,
            "resync_threshold": self._client_resync_threshold
        }

    def _increase_hotp_counter(self, count: int) -> None:
        redis_service.db(
            "hset", self._session_key, mapping={"count": count + 1}
        )
