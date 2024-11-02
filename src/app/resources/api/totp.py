from flask import abort

from src.app.resources.api import api
from src.app.schemas.totp import TOTPSchema
from src.app.services.totp import TOTPService
from src.app.schemas.common import schema_validation


@api.route("/totp", methods=["GET"])
@schema_validation(TOTPSchema)
def get_totp(**kwargs):
    service = TOTPService(**kwargs)
    if service.client_otp:
        status = service.verify()
        return {"status": status}
    else:
        uri = service.create()
        return {"uri": uri}

@api.route("/totp", methods=["DELETE"])
def delete_totp():
    service = TOTPService()
    if not service.delete():
        return abort(404, "HOTP not created")
    return {}, 204
