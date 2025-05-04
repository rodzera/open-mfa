from typing import Dict
from datetime import datetime

from src.app.configs.constants import APP_VERSION
from src.app.repositories.healthcheck import HealthCheckRepository


class HealthCheckService:
    """
    Controller and Application layer for healthcheck service.
    """
    def __init__(self):
        self.repo = HealthCheckRepository()

    def get_db_status(self) -> Dict:
        if db_datetime := self.repo.get_current_timestamp():
            return {
                "status": "up",
                "datetime": db_datetime,
                "version": self.repo.get_db_version()
            }
        else:
            return { "status": "down"}

    @staticmethod
    def get_server_status():
        return {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "up",
            "version": APP_VERSION
        }
