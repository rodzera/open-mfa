from uuid import uuid4
from flask import session
from datetime import timedelta

from src.app.utils.helpers.logs import get_logger
from src.app.services.redis import redis_service

log = get_logger(__name__)


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
