from src.app.utils.helpers.logging import get_logger
from src.app.services.user_session import UserSessionService

log = get_logger(__name__)


def trigger_user_session_service() -> None:
    UserSessionService().manage_session()
