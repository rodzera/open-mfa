from marshmallow import fields
from marshmallow.validate import Range

from src.app.schemas.oath.common import OTPValidationSchema, OTPFieldSchema


class HOTPSchema(OTPFieldSchema, OTPValidationSchema):
    # TODO : set a max window limit
    key = "hotp"
    initial_count = fields.Int(required=False, dump_default=0, validate=Range(min=0))
    resync_threshold = fields.Int(required=False, dump_default=5, validate=Range(min=5, max=10))
