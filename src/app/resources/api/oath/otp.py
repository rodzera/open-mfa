from src.app.resources.api import api
from src.app.services.oath import OTPService
from src.app.schemas.oath.otp import OTPSchema
from src.app.infra.middlewares.schemas import schema_middleware


@api.route("/otp", methods=["GET"])
@schema_middleware(OTPSchema)
def get_otp(**req_data):
    return OTPService(**req_data).get()
