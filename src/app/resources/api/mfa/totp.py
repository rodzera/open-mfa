from flask import abort

from src.app.resources.api import api
from src.app.schemas.mfa.totp import TOTPSchema
from src.app.services.mfa.totp import TOTPService
from src.app.schemas.mfa.common import schema_validation


@api.route("/totp", methods=["GET"])
@schema_validation(TOTPSchema)
def get_totp(**kwargs):
    service = TOTPService(**kwargs)
    return service.process_request()

@api.route("/totp", methods=["DELETE"])
def delete_totp():
    service = TOTPService()
    if not service.delete_data():
        return abort(404, "HOTP not created")
    return {}, 204
