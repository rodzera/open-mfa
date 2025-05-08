from flask import abort

from src.app.resources.api import api
from src.app.services.oath import HOTPService
from src.app.schemas.oath.hotp import HOTPSchema
from src.app.utils.helpers.logging import get_logger
from src.app.middlewares.schemas import schema_middleware

log = get_logger(__name__)


@api.route("/hotp", methods=["GET"])
@schema_middleware(HOTPSchema)
def get_hotp(**req_data):
    return HOTPService(**req_data).get()


@api.route("/hotp", methods=["DELETE"])
def delete_hotp():
    if HOTPService().delete():
        return {}, 204
    else:
        abort(404, "HOTP not created")
