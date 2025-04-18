from src.app.utils.helpers.logging import get_logger
from src.app.controllers.user_session import UserSessionController

log = get_logger(__name__)


def trigger_user_session_controller() -> None:
    log.debug("Triggering user session controller")
    UserSessionController.manage_session()
