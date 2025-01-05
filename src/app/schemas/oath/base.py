from typing import Optional
from werkzeug.exceptions import NotFound, Conflict
from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.app.services.oath.repositories import TOTPRepository, HOTPRepository


class OTPFieldSchema(Schema):
    otp = fields.Str(required=False)

    @validates("otp")
    def validate_otp_field(self, otp: Optional[str]) -> None:
        if not otp:
            return

        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError("OTP must be a 6-digit string")


class OTPValidationSchema(Schema):
    _service_type = None

    @post_load
    def validate(self, data, **kwargs):
        otp = data.get("otp")
        if self._service_type == "totp":
            session_data = TOTPRepository().check_session_data_exists()
        else:
            session_data = HOTPRepository().check_session_data_exists()


        if otp and not session_data:
            raise NotFound(f"{self._service_type.upper()} not created")
        elif not otp and session_data:
            raise Conflict(f"{self._service_type.upper()} already created")
        return data
