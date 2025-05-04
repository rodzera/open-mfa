from time import time
from pyotp import random_base32

from src.app.services.oath import BaseOTPService
from src.app.utils.helpers.logging import get_logger
from src.app.infra.aes_cipher import aes_cipher_infra
from src.app.domains.oath.otp import OTPEntity, OTPGenerator

log = get_logger(__name__)


class OTPService(BaseOTPService):
    service_type = "otp"

    def create(self) -> str:
        log.info(f"Starting {self.service_type.upper()} creation")

        raw_secret = random_base32()
        hash_secret = aes_cipher_infra.encrypt_b64(raw_secret)

        if self.session_data:
            entity = OTPEntity(
                self.session_data["code"],
                self.session_data["secret"],
                self.session_data["used"],
                self.session_data["creation_timestamp"],
            )
            if entity.is_valid:
                log.debug("Returning cached OTP")
                return entity.code

        log.debug("Creating new OTP")
        current_timestamp = int(time())
        server_code = OTPGenerator(raw_secret).generate_code(current_timestamp)
        entity = OTPEntity(
            server_code,
            hash_secret,
            used=0,
            timestamp=current_timestamp
        )
        self.repo.insert_session_data(entity.as_dict, exp=True)
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
            log.debug("OTP code is valid")
            entity.mark_as_used()
            self.repo.insert_session_data(entity.as_dict)
            return True
        else:
            log.debug("OTP code not valid")
            return False
