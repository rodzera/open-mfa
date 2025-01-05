from flask import abort
from typing import Optional
from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.app.infra.redis import redis_service


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
