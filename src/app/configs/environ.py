from typing import Dict
from datetime import timedelta

from app.logger import get_logger
from app.utils import terminate_server
from check_database import database_check

log = get_logger(__name__)


class DefaultConfig(object):
    def __init__(self, **kwargs):
        self.ADMIN_USER = self.DB_USER = "admin"
        self.JSON_SORT_KEYS = False
        self.REMEMBER_COOKIE_DURATION = timedelta(minutes=30)
        self.PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SWAGGER = dict(title="open-mfa", openapi="3.0.3")

    @property
    def supported_databases(self) -> Dict:
        return {
            "mysql": "pymysql",
            "postgresql": "psycopg2"
        }

    def db_uri(self, **kwargs) -> str:
        if (connector := self.supported_databases.get(kwargs["DB_PROVIDER"])) is None:
            raise ValueError("Invalid database provided")

        log.info("Testing database connection")
        if not database_check():
            terminate_server()

        log.info(f"Database: {kwargs['DB_PROVIDER'].upper()}")
        return f"{kwargs['DB_PROVIDER']}+{connector}://{self.DB_USER}:" \
               f"{kwargs['DB_PASS']}@{kwargs['DB_HOST']}/{kwargs['DB_DATABASE']}"

    @staticmethod
    def set_flask_config(**kwargs) -> object:
        if kwargs.get("TESTING"):
            return TestingConfig(**kwargs)
        elif kwargs.get("DEBUG"):
            return DevelopmentConfig(**kwargs)
        else:
            return ProductionConfig(**kwargs)


class DevelopmentConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to DEVELOPMENT mode")
        super().__init__(**kwargs)
        self.SQLALCHEMY_ECHO = True
        self.SQLALCHEMY_DATABASE_URI = self.db_uri(**kwargs)


class TestingConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to TESTING mode")
        super().__init__(**kwargs)
        self.ADMIN_PASS = "admin"
        self.SECRET_KEY = "ABCDEFGH12345678"
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        log.info("Database: in-memory SQLite")


class ProductionConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to PRODUCTION mode")
        super().__init__(**kwargs)
        self.SESSION_COOKIE_SECURE = True
        self.SQLALCHEMY_DATABASE_URI = self.db_uri(**kwargs)
