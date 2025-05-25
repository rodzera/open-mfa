from flask import abort

from src.app.resources.api import api
from src.app.services.oath import TOTPService
from src.app.schemas.oath.totp import TOTPSchema
from src.app.utils.helpers.logging import get_logger
from src.app.middlewares.schemas import schema_middleware

log = get_logger(__name__)


@api.route("/totp", methods=["GET"])
@schema_middleware(TOTPSchema)
def get_totp(**req_data):
    return TOTPService(**req_data).get()


@api.route("/totp", methods=["DELETE"])
def delete_totp():
    if TOTPService().delete():
        return {}, 204
    else:
        abort(404, "TOTP not created")
