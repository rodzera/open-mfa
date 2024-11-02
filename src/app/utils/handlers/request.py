from uuid import uuid4
from datetime import timedelta
from flask import Response, session

from src.app.logger import get_logger
from src.app.services.redis import redis_service


log = get_logger(__name__)

__all__ = [
    "set_session_id_before_request",
    "log_json_after_request"
]

def set_session_id_before_request() -> None:
    """
    Generates a unique session ID for new sessions and saves it in the session
    object and Redis for tracking OTPs.
    """
    if "session_id" not in session:
        session_id = str(uuid4())
        log.debug(f"Creating session id: {session_id}")

        session["session_id"] = session_id
        session.permanent = True
        redis_service.db(
            "setex", f"session:{session_id}", timedelta(minutes=30), "active"
        )

def log_json_after_request(response: Response) -> Response:
    if response.get_json(silent=True):
        log.debug(f"Returning response: {response.json}")
    return response
