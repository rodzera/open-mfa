from functools import wraps
from flask import request, abort, current_app

from src.app.logger import get_logger

log = get_logger(__name__)

__all__ = ["admin_auth"]

def admin_auth():
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            log.info(f"Authentication required called: {request.endpoint}")
            auth = request.authorization
            if not auth or not hasattr(auth, "username") or not hasattr(auth, "password"):
                log.debug("Invalid authorization in headers")
                abort(401)
            if auth.username != current_app.config["ADMIN_USER"] or auth.password != \
                    current_app.config["ADMIN_PASS"]:
                log.debug("Invalid super admin credential")
                abort(401)
            return func(*args, **kwargs)
        return wrap
    return decorator
