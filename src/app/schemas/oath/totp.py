from marshmallow import fields
from marshmallow.validate import Range

from src.app.configs.oath import TOTP_DF_CONFIG
from src.app.schemas.oath.base import OTPValidationSchema, OTPFieldSchema


class TOTPSchema(OTPFieldSchema, OTPValidationSchema):
    service_type = "totp"
    interval = fields.Int(
        required=False,
        load_default=TOTP_DF_CONFIG["min_interval"],
        validate=Range(
            min=TOTP_DF_CONFIG["min_interval"],
            max=TOTP_DF_CONFIG["max_interval"]
        )
    )
