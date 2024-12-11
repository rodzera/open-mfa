from flask import abort

from src.app.resources.api import api
from src.app.schemas.mfa.hotp import HOTPSchema
from src.app.services.mfa.hotp import HOTPService
from src.app.schemas.mfa.common import schema_validation


@api.route("/hotp", methods=["GET"])
@schema_validation(HOTPSchema)
def get_hotp(**kwargs):
    service = HOTPService(**kwargs)
    return service.process_request()

@api.route("/hotp", methods=["DELETE"])
def delete_hotp():
    service = HOTPService()
    if not service.delete_data():
        return abort(404, "HOTP not created")
    return {}, 204
