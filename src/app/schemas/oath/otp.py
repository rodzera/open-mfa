from marshmallow import post_load
from werkzeug.exceptions import NotFound

from src.app.repositories.oath import OTPRepository
from src.app.schemas.oath.base import OTPFieldSchema


class OTPSchema(OTPFieldSchema):
    service_type = "otp"

    @post_load
    def otp_validation(self, data, **kwargs):
        if not data.get("otp"):
            return data

        session_data = OTPRepository(self.service_type).session_data_exists()
        if not session_data:
            raise NotFound("OTP not created")
        return data
