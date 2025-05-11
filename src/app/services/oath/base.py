from abc import ABC, abstractmethod

from src.app.configs.types import OTPType
from src.app.repositories.oath import OATHRepository
from src.app.services.oath.cipher import OATHCipherService
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class OATHService(ABC):
    """
    Controller and Application layer class for OATH services.
    """
    cache: dict = None
    service_type: OTPType
    repo: OATHRepository = OATHRepository
    cipher: OATHCipherService = OATHCipherService

    @property
    def session_data(self):
        if not self.cache:
            self.cache = self.repo.get_session_data()
        return self.cache

    @session_data.setter
    def session_data(self, data):
        self.cache = data

    def __init__(self, **req_data):
        self.repo = self.repo(self.service_type)
        self.cipher = self.cipher()
        self.req_data = req_data
        self.req_otp = req_data.get("otp")

    def get(self) -> dict:
        if self.req_otp:
            return {"status": self.verify()}
        else:
            key = "otp" if self.service_type == "otp" else "uri"
            return {key: self.create()}

    def delete(self) -> bool:
        log.info(f"Starting {self.service_type.upper()} deletion")
        if not self.session_data:
            log.debug(f"No {self.service_type.upper()} data found")
            return False

        result = bool(self.repo.delete_session_data())
        log.info(f"{self.service_type.upper()} deletion: {result}")
        return result

    @abstractmethod
    def create(self) -> str:
        pass

    @abstractmethod
    def verify(self) -> bool:
        pass
