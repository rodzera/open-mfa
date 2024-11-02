from flask import jsonify

from src.app.resources.api import api


@api.route("/totp", methods=["GET"])
def get_totp():
    return jsonify({})
