from typing import Dict
from datetime import datetime

from src.app.infra.redis import redis_service
from src.app.configs.constants import APP_VERSION
from src.app.repositories.healthcheck import HealthCheckRepository


class HealthCheckController:

    @staticmethod
    def get_db_status() -> Dict:
        if db_datetime := redis_service.current_timestamp:
            return {
                "status": "up",
                "datetime": db_datetime,
                "version": HealthCheckRepository.get_db_version()
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
