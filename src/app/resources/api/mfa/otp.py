from src.app.resources.api import api
from src.app.schemas.mfa.otp import OTPSchema
from src.app.services.mfa.otp import OTPService
from src.app.schemas.mfa.common import schema_validation


@api.route("/otp", methods=["GET"])
@schema_validation(OTPSchema)
def get_otp(**kwargs):
    service = OTPService(**kwargs)
    return service.process_request()
