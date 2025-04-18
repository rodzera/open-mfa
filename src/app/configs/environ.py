from src.app.utils.helpers.logging import get_logger
from src.app.services.user_session import UserSessionService

log = get_logger(__name__)


class DefaultConfig(object):
    def __init__(self, **kwargs):
        self.JSON_SORT_KEYS = False
        self.REMEMBER_COOKIE_DURATION = UserSessionService.SESSION_EXP_TIME
        self.PERMANENT_SESSION_LIFETIME = UserSessionService.SESSION_EXP_TIME
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
        self.ENV = "development"


class TestingConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to TESTING env")
        super().__init__(**kwargs)
        self.ENV = "testing"
        self.ADMIN_USER = self.ADMIN_PASS = "admin"
        self.SECRET_KEY = "ABCDEFGH12345678"


class ProductionConfig(DefaultConfig):
    def __init__(self, **kwargs):
        log.info("Setting flask config to PRODUCTION env")
        super().__init__(**kwargs)
        self.ENV = "production"
        self.SESSION_COOKIE_SECURE = True
