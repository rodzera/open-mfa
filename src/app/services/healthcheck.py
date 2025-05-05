from datetime import datetime

from src.app.configs.constants import APP_VERSION
from src.app.utils.helpers.logging import get_logger
from src.app.repositories.healthcheck import HealthCheckRepository

log = get_logger(__name__)


class HealthCheckService:
    """
    Controller and Application layer for healthcheck service.
    """
    def __init__(self):
        self.repo = HealthCheckRepository()

    def get_db_status(self) -> dict:
        log.info("Checking database status")
        if db_datetime := self.repo.get_current_timestamp():
            response = {
                "status": "up",
                "datetime": db_datetime,
                "version": self.repo.get_db_version()
            }
        else:
            response = {"status": "down"}

        log.info(f"Database status: {response['status']}")
        return response

    @staticmethod
    def get_server_status():
        response = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "up",
            "version": APP_VERSION
        }
        log.debug(f"Returning server status: {response}")
        return response
