from marshmallow import fields
from marshmallow.validate import Range

from src.app.schemas.mfa.common import OTPValidationSchema, OTPFieldSchema


class HOTPSchema(OTPFieldSchema, OTPValidationSchema):
    # TODO : set a max window for HOTP
    initial_count = fields.Int(required=False, dump_default=0, validate=Range(min=0))
    key = "hotp"
