from flask import request
from functools import wraps
from typing import Callable, Type

from marshmallow import Schema


def schema_middleware(schema_class: Type[Schema]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            client_data = request.args if not request.is_json else request.json
            validated_data = schema.load(client_data)
            kwargs.update(validated_data)
            return func(*args, **kwargs)
        return wrapper
    return decorator
