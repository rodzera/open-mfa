from marshmallow import ValidationError
from werkzeug import Response as WerkzeugResponse
from flask import json, Flask, Response as FlaskResponse
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from src.app.logger import get_logger
from src.app.utils.helpers.json import jsonify_error_response

log = get_logger(__name__)

__all__ = ["register_error_handlers"]


def handle_any_error(e: HTTPException) -> WerkzeugResponse:
    log.error(f"Handling error: {e.__repr__()}")
    response = e.get_response()
    data = dict(status_code=e.code, name=e.name, message=e.description)
    log.error(f"Error handled. Returning Response: {data}")
    response.data = json.dumps(data)
    response.mimetype = "application/json"
    return response


def handle_any_exception(e: BaseException) -> FlaskResponse:
    log.debug(f"Handling exception: {e}")
    if isinstance(e, HTTPException):
        return e
    if isinstance(e, ValidationError):
        log.exception(f"Marshmallow validation error: {e.messages}")
        return jsonify_error_response(400, "Bad Request", e.messages)
    log.exception(f"Uncaught Exception occurred: {e}")
    return jsonify_error_response(500, "Internal Server Error", InternalServerError.description)


def register_error_handlers(app: Flask):
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_any_error)
    app.register_error_handler(Exception, handle_any_exception)
