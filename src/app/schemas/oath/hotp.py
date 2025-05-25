from marshmallow import fields
from marshmallow.validate import Range

from src.core.configs.base import OATH_CONFIG
from src.app.schemas.oath.base import OTPValidationSchema, OATHSchema


class HOTPSchema(OATHSchema, OTPValidationSchema):
    # TODO : set a max window limit
    service_type = "hotp"
    initial_count = fields.Int(required=False, load_default=0, validate=Range(min=0))
    resync_threshold = fields.Int(
        required=False,
        load_default=OATH_CONFIG.hotp.min_resync_threshold,
        validate=Range(
            min=OATH_CONFIG.hotp.min_resync_threshold,
            max=OATH_CONFIG.hotp.max_resync_threshold
        )
    )
