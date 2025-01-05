from marshmallow import fields
from marshmallow.validate import Range

from src.app.configs.oath import HOTP_DF_CONFIG
from src.app.schemas.oath.base import OTPValidationSchema, OTPFieldSchema


class HOTPSchema(OTPFieldSchema, OTPValidationSchema):
    # TODO : set a max window limit
    _service_type = "hotp"
    initial_count = fields.Int(required=False, dump_default=0, validate=Range(min=0))
    resync_threshold = fields.Int(
        required=False,
        dump_default=HOTP_DF_CONFIG["min_resync_threshold"],
        validate=Range(
            min=HOTP_DF_CONFIG["min_resync_threshold"],
            max=HOTP_DF_CONFIG["max_resync_threshold"]
        )
    )
