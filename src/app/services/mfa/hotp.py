from pyotp import HOTP
from typing import Dict
from flask import session

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service
from src.app.services.mfa.base import BaseOTPService

log = get_logger(__name__)


class HOTPService(BaseOTPService):
    _service_type = "hotp"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client_initial_count = kwargs.get("initial_count", 0)
        self._cached_count = int(self._service_data.get("count", 0))
        self._server_hotp = HOTP(self._secret, initial_count=self._client_initial_count)
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
        status = self._server_hotp.verify(self._client_otp, self._cached_count)
        if status:
            self._increase_hotp_counter()
        return {"status": status}

    @property
    def _default_data(self) -> Dict:
        return {
            "count": self._client_initial_count,
            "secret": self._secret,
            "uri": self._hotp_uri
        }

    def _increase_hotp_counter(self) -> None:
        redis_service.db(
            "hset", self._session_key, mapping={"count": self._cached_count + 1}
        )
