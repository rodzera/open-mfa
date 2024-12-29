from flask import abort
from marshmallow import post_load

from src.app.services.redis import redis_service
from src.app.schemas.oath.common import OTPFieldSchema


class OTPSchema(OTPFieldSchema):

    @post_load
    def otp_validation(self, data, **kwargs):
        if not data.get("otp"):
            return data

        redis_key = redis_service.get_session_key("otp")
        if not redis_service.db("exists", redis_key):
            abort(404, "OTP not created")
        return data
