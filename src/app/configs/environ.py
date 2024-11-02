from datetime import timedelta

from src.app.logger import get_logger

log = get_logger(__name__)


class DefaultConfig(object):
    def __init__(self, **kwargs):
        self.ADMIN_USER = "admin"
        self.JSON_SORT_KEYS = False
        self.REMEMBER_COOKIE_DURATION = timedelta(minutes=60)
        self.PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
        self.SWAGGER = dict(title="open-mfa", openapi="3.0.3")

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
        log.info("Setting flask config to DEVELOPMENT env")
        super().__init__(**kwargs)


class TestingConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to TESTING env")
        super().__init__(**kwargs)
        self.ADMIN_PASS = "admin"
        self.SECRET_KEY = "ABCDEFGH12345678"


class ProductionConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to PRODUCTION env")
        super().__init__(**kwargs)
        self.SESSION_COOKIE_SECURE = True
