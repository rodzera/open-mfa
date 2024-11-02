from flask import abort
from marshmallow import Schema, fields, validates, ValidationError

from src.app.services.redis import redis_service


class OTPSchema(Schema):
    otp = fields.Str(required=False)

    @validates('otp')
    def validate_otp(self, otp):
        if not otp:
            return

        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError("OTP must be a 6-digit string")

        redis_key = redis_service.get_session_key("otp")
        if not redis_service.db("exists", redis_key):
            abort(404, "OTP not created")
