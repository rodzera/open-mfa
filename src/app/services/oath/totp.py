from pyotp import random_base32
from src.app.services.oath import BaseOTPService
from src.app.utils.helpers.logging import get_logger
from src.app.infra.aes_cipher import aes_cipher_infra
from src.core.entities.totp_entity import TOTPEntity
from src.core.services.totp_generator import TOTPGenerator

log = get_logger(__name__)


class TOTPService(BaseOTPService):
    service_type = "totp"

    def create(self) -> str:
        log.info(f"Starting {self.service_type.upper()} creation")

        raw_secret = random_base32()
        hash_secret = aes_cipher_infra.encrypt_b64(raw_secret)

        entity = TOTPEntity(hash_secret, self.req_data["interval"])
        self.repo.insert_session_data(entity.as_dict, exp=True)

        generator = TOTPGenerator(raw_secret, entity.interval)
        return generator.generate_uri(session_id=self.repo.user_session_id)

    def verify(self) -> bool:
        log.info(f"Starting {self.service_type.upper()} verifying")

        hash_secret = self.session_data["secret"]
        raw_secret = aes_cipher_infra.decrypt_b64(hash_secret)

        entity = TOTPEntity(
            hash_secret,
            self.session_data["interval"],
            self.session_data["last_used_otp"]
        )
        generator = TOTPGenerator(raw_secret, entity.interval)

        if generator.verify(self.req_otp) and not entity.is_replay(self.req_otp):
            log.debug("TOTP code is valid")
            entity.accept_otp(self.req_otp)
            self.repo.insert_session_data(entity.as_dict)
            return True
        else:
            log.debug("TOTP code not valid")
            return False
