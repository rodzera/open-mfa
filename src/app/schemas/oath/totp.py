from marshmallow import fields
from marshmallow.validate import Range

from src.app.schemas.oath.common import OTPValidationSchema, OTPFieldSchema


class TOTPSchema(OTPFieldSchema, OTPValidationSchema):
    key = "totp"
    interval = fields.Int(required=False, dump_default=30, validate=Range(min=30, max=60))
