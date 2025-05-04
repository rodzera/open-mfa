from typing import Callable
from functools import wraps
from flask import request, abort

from src.app.utils.helpers.logging import get_logger
from src.app.services.auth import authenticate_super_admin

log = get_logger(__name__)


def auth_middleware(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        log.info(f"Authentication middleware called: {request.endpoint}")
        auth = request.authorization
        if not auth or not hasattr(auth, "username") or not hasattr(auth, "password"):
            log.debug("Invalid or missing authorization in headers")
            abort(401, "Unauthorized")
        if not authenticate_super_admin(auth):
            log.debug("Invalid credentials in headers")
            abort(401, "Unauthorized")
        return func(*args, **kwargs)
    return wrapper
