from time import time

from src.app.services.oath import OATHService
from src.core.entities.otp_entity import OTPEntity
from src.app.utils.helpers.logging import get_logger
from src.core.services.otp_generator import OTPGenerator

log = get_logger(__name__)


class OTPService(OATHService):
    service_type = "otp"

    def create(self) -> str:
        log.info(f"Starting {self.service_type.upper()} creation")
        raw_secret, hash_secret = self.cipher.generate_secret()

        if self.session_data:
            entity = OTPEntity(
                self.session_data["code"],
                self.session_data["secret"],
                self.session_data["used"],
                self.session_data["creation_timestamp"],
            )
            if entity.is_valid:
                log.info("Returning cached OTP")
                return entity.code

        log.info("Creating new OTP")
        current_timestamp = int(time())
        server_code = OTPGenerator(raw_secret).generate_code(current_timestamp)
        entity = OTPEntity(
            server_code,
            hash_secret,
            used=0,
            timestamp=current_timestamp
        )
        log.debug("Storing OTP data in repository")
        self.repo.insert_session_data(entity.as_dict, exp=True)
        log.debug("OTP stored successfully")
        return entity.code

    def verify(self) -> bool:
        log.info(f"Starting {self.service_type.upper()} verifying")
        entity = OTPEntity(
            self.session_data["code"],
            self.session_data["secret"],
            self.session_data["used"],
            self.session_data["creation_timestamp"],
        )
        if entity.code == self.req_otp and entity.is_valid:
            log.info("OTP code is valid")
            entity.mark_as_used()
            self.repo.insert_session_data(entity.as_dict)
            return True
        else:
            log.info("OTP code not valid")
            return False
