from flask import request
from logging import getLevelName, root

from src.app.resources.api import api
from src.app.schemas.logs import LogSchema
from src.app.infra.middlewares.auth import admin_auth

schema = LogSchema()


@api.route("/logs", methods=["GET"])
@admin_auth()
def get_logger_level():
    return {"level": getLevelName(root.level)}, 200


@api.route("/logs", methods=["PUT"])
@admin_auth()
def set_logger_level():
    return schema.load(request.json)
