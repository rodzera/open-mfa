from flask import abort

from src.app.resources.api import api
from src.app.schemas.oath.hotp import HOTPSchema
from src.app.infra.middlewares.schemas import schema_validation
from src.app.services.oath.services.hotp_service import HOTPService


@api.route("/hotp", methods=["GET"])
@schema_validation(HOTPSchema)
def get_hotp(**kwargs):
    service = HOTPService(**kwargs)
    return service.process_request()

@api.route("/hotp", methods=["DELETE"])
def delete_hotp():
    service = HOTPService()
    if not service.delete_data():
        abort(404, "HOTP not created")
    return {}, 204
