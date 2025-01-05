from src.app.resources.api import api
from src.app.schemas.oath.otp import OTPSchema
from src.app.infra.middlewares.schemas import schema_middleware
from src.app.services.oath.services.otp_service import OTPService


@api.route("/otp", methods=["GET"])
@schema_middleware(OTPSchema)
def get_otp(**kwargs):
    service = OTPService(**kwargs)
    return service.process_request()
