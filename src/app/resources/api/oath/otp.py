from src.app.resources.api import api
from src.app.schemas.oath.otp import OTPSchema
from src.app.services.oath.otp import OTPService
from src.app.schemas.oath.common import schema_validation


@api.route("/otp", methods=["GET"])
@schema_validation(OTPSchema)
def get_otp(**kwargs):
    service = OTPService(**kwargs)
    return service.process_request()
