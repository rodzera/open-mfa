from flask import request
from functools import wraps
from typing import Callable, Type

from marshmallow import Schema


def schema_middleware(schema_class: Type[Schema]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            client_data = schema.load(request.args)
            kwargs.update(client_data)
            return func(*args, **kwargs)
        return wrapper
    return decorator
