from marshmallow import fields
from marshmallow.validate import Range

from src.core.configs.base import OATH_CONFIG
from src.app.schemas.oath.base import OTPValidationSchema, OATHSchema


class TOTPSchema(OATHSchema, OTPValidationSchema):
    service_type = "totp"
    interval = fields.Int(
        required=False,
        load_default=OATH_CONFIG.totp.min_interval,
        validate=Range(
            min=OATH_CONFIG.totp.min_interval,
            max=OATH_CONFIG.totp.max_interval
        )
    )
