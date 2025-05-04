from typing import Optional
from flask import has_request_context, session as flask_session
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


class UserSessionRepository:
    def __init__(self) -> None:
        self.repo = flask_session

    def get_session_id(self) -> Optional[str]:
        if has_request_context():
            return self.repo.get("session_id")

    def save_session(self, session_id: str) -> None:
        if has_request_context():
            self.repo["session_id"] = session_id
            self.repo.permanent = True
