from functools import wraps
from flask import abort, request, Response

from src.app.logger import get_logger


log = get_logger(__name__)

__all__ = ["log_json_after_request", "request_validator"]


def log_json_after_request(response: Response) -> Response:
    if response.get_json(silent=True):
        log.debug(f"Returning response: {response.json}")
    return response


def request_validator():
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            log.debug({
                "request": {
                    "endpoint": getattr(request, "endpoint"),
                    "method": getattr(request, "method"),
                    "headers": getattr(request, "headers"),
                    "content_type": getattr(request, "content_type"),
                }
            })

            if not request.accept_mimetypes["application/json"]:
                log.error("Invalid accept headers in request")
                abort(406)

            if request.method not in ["POST", "PUT"]:
                return func(*args, **kwargs)

            if getattr(request, "content_type") != "application/json":
                log.exception(f"Mimetype not supported: {request.mimetype}")
                abort(501)

            if not (data := request.get_json(silent=True)):
                abort(400, "Missing json data")
            log.debug(f"Request payload: {data}")

            return func(*args, **kwargs)
        return wrap
    return decorator
