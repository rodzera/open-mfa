from flask import abort
from marshmallow.validate import Range
from marshmallow import fields, post_load

from src.app.schemas.otp import OTPSchema
from src.app.services.redis import redis_service


class HOTPSchema(OTPSchema):
    initial_count = fields.Int(required=False, default=0, validate=Range(min=0))

    @post_load
    def validate(self, data, **kwargs):
        otp = data.get("otp")
        redis_key = redis_service.get_session_key("hotp")
        hotp_data = redis_service.db("exists", redis_key)

        if otp and not hotp_data:
            abort(404, "HOTP not created")
        elif not otp and hotp_data:
            abort(409, "HOTP already created")
        return data
