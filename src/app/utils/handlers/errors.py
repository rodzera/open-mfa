from redis import RedisError
from marshmallow import ValidationError
from flask import json, Flask, Response as FlaskResponse
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from src.app.utils.helpers.logs import get_logger
from src.app.utils.helpers.json import jsonify_error_response

log = get_logger(__name__)

__all__ = ["register_error_handlers"]


def handle_marshmallow_exc(e: ValidationError) -> FlaskResponse:
    log.error(f"Marshmallow validation error: {e.messages}")
    first_error = list(e.messages.values())[0][0]
    return jsonify_error_response(400, "Bad Request", first_error)

def handle_redis_exc(e: RedisError) -> FlaskResponse:
    return make_500_response("Redis exception occurred")

def handle_any_exc(e: BaseException) -> FlaskResponse:
    return make_500_response()

def make_500_response(msg: str = "Uncaught exception occurred"):
    log.exception(f"{msg}:")
    return jsonify_error_response(
        500,
        "Internal Server Error",
        InternalServerError.description
    )

def handle_any_error(e: HTTPException) -> FlaskResponse:
    log.error(f"Handling error: {e.__repr__()}")
    response = e.get_response()
    data = dict(code=e.code, name=e.name, description=e.description)
    log.error(f"Error handled. Returning Response: {data}")
    response.data = json.dumps(data)
    response.mimetype = "application/json"
    return response

def register_error_handlers(app: Flask):
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_any_error)
    app.register_error_handler(ValidationError, handle_marshmallow_exc)
    app.register_error_handler(RedisError, handle_redis_exc)
    app.register_error_handler(Exception, handle_any_exc)
