from marshmallow import fields
from marshmallow.validate import Range

from src.app.schemas.common import OTPValidationSchema, OTPFieldSchema


class TOTPSchema(OTPFieldSchema, OTPValidationSchema):
    interval = fields.Int(required=False, default=30, validate=Range(min=30, max=60))
    key = "totp"
