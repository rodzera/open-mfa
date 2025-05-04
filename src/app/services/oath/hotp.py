from pyotp import random_base32
from src.app.services.oath import BaseOTPService
from src.app.utils.helpers.logging import get_logger
from src.app.infra.aes_cipher import aes_cipher_infra
from src.core.entities.hotp_entity import HOTPEntity
from src.core.services.hotp_generator import HOTPGenerator

log = get_logger(__name__)


class HOTPService(BaseOTPService):
    service_type = "hotp"

    def create(self) -> str:
        log.info(f"Starting {self.service_type.upper()} creation")

        raw_secret = random_base32()
        hash_secret = aes_cipher_infra.encrypt_b64(raw_secret)

        entity = HOTPEntity(
            hash_secret,
            self.req_data["initial_count"],
            self.req_data["resync_threshold"]
        )
        self.repo.insert_session_data(entity.as_dict, exp=True)

        generator = HOTPGenerator(raw_secret, entity.count)
        return generator.generate_uri(session_id=self.repo.user_session_id)

    def verify(self) -> bool:
        log.info(f"Starting {self.service_type.upper()} verifying")

        hash_secret = self.session_data["secret"]
        raw_secret = aes_cipher_infra.decrypt_b64(hash_secret)

        entity = HOTPEntity(
            hash_secret,
            self.session_data["count"],
            self.session_data["resync_threshold"]
        )
        generator = HOTPGenerator(raw_secret, entity.count)

        if generator.verify(self.req_otp):
            log.debug("HOTP code is valid")
            entity.increment(1)
            self.repo.insert_session_data(entity.as_dict)
            return True

        status, new_count = generator.resync_protocol(
            self.req_otp, entity.resync_threshold
        )
        if status:
            entity.increment(new_count)
            self.repo.insert_session_data(entity.as_dict)
            return True

        log.debug("HOTP code not valid")
        return False
