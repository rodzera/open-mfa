from src.app.services.oath import OATHService
from src.core.entities.hotp import HOTPEntity
from src.infra.adapters.hotp import HOTPGenerator
from src.core.rules.hotp_resync import HOTPResyncService
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class HOTPService(OATHService):
    service_type = "hotp"

    def create(self) -> str:
        log.info(f"Starting {self.service_type.upper()} creation")
        raw_secret, hash_secret = self.cipher.generate_secret()

        entity = HOTPEntity(
            hash_secret,
            self.req_data["initial_count"],
            self.req_data["resync_threshold"]
        )
        log.info("Storing HOTP data in repository")
        self.repo.insert_session_data(entity.as_dict, exp=True)
        log.info("HOTP stored successfully")

        generator = HOTPGenerator(raw_secret, entity.count)
        return generator.generate_uri(session_id=self.repo.user_session_id)

    def verify(self) -> bool:
        log.info(f"Starting {self.service_type.upper()} verifying")

        hash_secret = self.session_data["secret"]
        raw_secret = self.cipher.decrypt_secret(hash_secret)

        entity = HOTPEntity(
            hash_secret,
            self.session_data["count"],
            self.session_data["resync_threshold"]
        )
        generator = HOTPGenerator(raw_secret, entity.count)

        if generator.verify(self.req_otp):
            log.info("HOTP code is valid")
            entity.increment(1)
            self.repo.insert_session_data(entity.as_dict)
            return True

        hotp_resync_service = HOTPResyncService(generator)
        status, new_count = hotp_resync_service.resync(
            self.req_otp, entity.resync_threshold
        )
        if status:
            entity.increment(new_count)
            log.info("Updating HOTP data in repository")
            self.repo.insert_session_data(entity.as_dict)
            return True

        log.info("HOTP code not valid")
        return False
