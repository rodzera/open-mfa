from flask import make_response, Response

from src.app.utils.helpers.logs import get_logger

log = get_logger(__name__)


def jsonify_error_response(code: int, name: str, description: str) -> Response:
    payload = dict(code=code, name=name, description=description)
    log.debug(f"Exception handled. Returning response: {payload}")
    response = make_response(payload)
    response.status = code
    return response
