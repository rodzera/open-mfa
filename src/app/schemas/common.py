from typing import Optional
from functools import wraps
from flask import abort, request
from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.app.services.redis import redis_service


def schema_validation(schema_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            client_data = schema.load(request.args)
            kwargs.update(client_data)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class OTPFieldSchema(Schema):
    otp = fields.Str(required=False)

    @validates("otp")
    def validate_otp_field(self, otp: Optional[str]) -> None:
        if not otp:
            return

        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError("OTP must be a 6-digit string")


class OTPValidationSchema(Schema):
    key = None

    @post_load
    def validate(self, data, **kwargs):
        otp = data.get("otp")
        redis_key = redis_service.get_session_key(self.key)
        totp_data = redis_service.db("exists", redis_key)

        if otp and not totp_data:
            abort(404, f"{self.key.upper()} not created")
        elif not otp and totp_data:
            abort(409, f"{self.key.upper()} already created")
        return data
