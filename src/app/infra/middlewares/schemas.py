from flask import request
from typing import Callable
from functools import wraps


def schema_validation(schema_class) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            client_data = schema.load(request.args)
            kwargs.update(client_data)
            return func(*args, **kwargs)
        return wrapper
    return decorator
