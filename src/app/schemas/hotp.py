from marshmallow import fields
from marshmallow.validate import Range

from src.app.schemas.common import OTPValidationSchema, OTPFieldSchema


class HOTPSchema(OTPFieldSchema, OTPValidationSchema):
    # TODO : set a window max for HOTP
    initial_count = fields.Int(required=False, default=0, validate=Range(min=0))
    key = "hotp"
