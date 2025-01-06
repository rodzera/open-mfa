from src.app.utils.helpers.logging import get_logger
from src.app.services.user_session import UserSessionService

log = get_logger(__name__)


class UserSessionController:

    @staticmethod
    def manage_session() -> str:
        user_session = UserSessionService()
        if not user_session.is_active():
            user_session.create_session()
        return user_session.session_id
