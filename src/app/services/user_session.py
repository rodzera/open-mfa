from uuid import uuid4
from datetime import timedelta
from flask import has_request_context

from src.app.utils.helpers.logging import get_logger
from src.app.repositories.user_session import UserSessionRepository

log = get_logger(__name__)


class UserSessionService:
    SESSION_EXP_TIME = timedelta(hours=1)

    def __init__(self):
        self.repository = UserSessionRepository()
        self.session_id = self.repository.get_session_id()

    def is_active(self) -> bool:
        return self.session_id is not None

    def create_session(self) -> None:
        if has_request_context():
            self.session_id = str(uuid4())
            log.debug(f"Creating new user session: {self.session_id}")
            self.repository.save_session(self.session_id)
