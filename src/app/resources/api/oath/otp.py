from src.app.resources.api import api
from src.app.schemas.oath.otp import OTPSchema
from src.app.infra.middlewares import schema_validation
from src.app.services.oath.services.otp_service import OTPService


@api.route("/otp", methods=["GET"])
@schema_validation(OTPSchema)
def get_otp(**kwargs):
    service = OTPService(**kwargs)
    return service.process_request()
