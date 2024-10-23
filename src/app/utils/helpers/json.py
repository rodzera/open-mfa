from flask import make_response, Response

from src.app.logger import get_logger

log = get_logger(__name__)

__all__ = ["jsonify_success_response", "jsonify_error_response"]


def jsonify_success_response(status_code: int = 200) -> Response:
    response = make_response({"status": "success"})
    response.status = status_code
    return response


def jsonify_error_response(status_code: int, name: str, message: str) -> Response:
    _json = dict(status_code=status_code, name=name, message=message)
    log.debug(f"Exception handled. Returning response: {_json}")
    response = make_response(_json)
    response.status = status_code
    return response
