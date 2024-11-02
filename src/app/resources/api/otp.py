from src.app.resources.api import api
from src.app.services.otp import OTPService
from src.app.schemas.otp import OTPSchema
from src.app.schemas.common import schema_validation


@api.route("/otp", methods=["GET"])
@schema_validation(OTPSchema)
def get_otp(**kwargs):
    service = OTPService(**kwargs)
    if service.client_otp:
        status = service.verify()
        return {"status": status}
    else:
        otp = service.create()
        return {"otp": otp}
