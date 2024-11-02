from flask import jsonify

from src.app.resources.api import api


@api.route("/hotp", methods=["GET"])
def get_hotp():
    return jsonify({})
