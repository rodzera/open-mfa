from src.app.services.oath import OATHService
from src.core.entities.totp_entity import TOTPEntity
from src.core.services.totp_generator import TOTPGenerator
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class TOTPService(OATHService):
    service_type = "totp"

    def create(self) -> str:
        log.info(f"Starting {self.service_type.upper()} creation")
        raw_secret, hash_secret = self.cipher.generate_secret()

        entity = TOTPEntity(hash_secret, self.req_data["interval"])
        log.info("Storing TOTP data in repository")
        self.repo.insert_session_data(entity.as_dict, exp=True)
        log.info("TOTP stored successfully")

        generator = TOTPGenerator(raw_secret, entity.interval)
        return generator.generate_uri(session_id=self.repo.user_session_id)

    def verify(self) -> bool:
        log.info(f"Starting {self.service_type.upper()} verifying")

        hash_secret = self.session_data["secret"]
        raw_secret = self.cipher.decrypt_secret(hash_secret)

        entity = TOTPEntity(
            hash_secret,
            self.session_data["interval"],
            self.session_data["last_used_otp"]
        )
        generator = TOTPGenerator(raw_secret, entity.interval)

        if generator.verify(self.req_otp) and not entity.is_replay(self.req_otp):
            log.info("TOTP code is valid")
            entity.accept_otp(self.req_otp)

            log.info("Updating TOTP data in repository")
            self.repo.insert_session_data(entity.as_dict)
            return True
        else:
            log.info("TOTP code not valid")
            return False
