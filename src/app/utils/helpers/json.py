from flask import make_response, Response

from src.app.logger import get_logger

log = get_logger(__name__)

__all__ = ["jsonify_error_response"]


def jsonify_error_response(code: int, name: str, description: str) -> Response:
    _json = dict(code=code, name=name, description=description)
    log.debug(f"Exception handled. Returning response: {_json}")
    response = make_response(_json)
    response.status = code
    return response
