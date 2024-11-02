from flask import abort

from src.app.resources.api import api
from src.app.schemas.hotp import HOTPSchema
from src.app.services.hotp import HOTPService
from src.app.schemas.common import schema_validation


@api.route("/hotp", methods=["GET"])
@schema_validation(HOTPSchema)
def get_hotp(**kwargs):
    service = HOTPService(**kwargs)
    if service.client_otp:
        status = service.verify()
        return {"status": status}
    else:
        uri = service.create()
        return {"uri": uri}

@api.route("/hotp", methods=["DELETE"])
def delete_hotp():
    service = HOTPService()
    if not service.delete():
        return abort(404, "HOTP not created")
    return {}, 204
