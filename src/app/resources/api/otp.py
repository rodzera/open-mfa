from src.app.resources.api import api
from src.app.services.otp import OTPService
from src.app.schemas.otp import OTPSchema
from src.app.schemas.common import schema_validation


@api.route("/otp", methods=["GET"])
@schema_validation(OTPSchema)
def otp_route(**kwargs):
    service = OTPService(**kwargs)
    if not service.client_otp:
        otp = service.create_flow()
        return {"otp": otp}
    else:
        status = service.verify_flow()
        return {"status": status}
