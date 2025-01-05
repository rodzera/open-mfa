from flask import abort

from src.app.resources.api import api
from src.app.schemas.oath.totp import TOTPSchema
from src.app.infra.middlewares.schemas import schema_middleware
from src.app.services.oath.services.totp_service import TOTPService


@api.route("/totp", methods=["GET"])
@schema_middleware(TOTPSchema)
def get_totp(**client_data):
    service = TOTPService(**client_data)
    return service.process_request()

@api.route("/totp", methods=["DELETE"])
def delete_totp():
    service = TOTPService()
    if not service.delete_data():
        abort(404, "TOTP not created")
    return {}, 204
