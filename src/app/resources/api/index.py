from flask import redirect, url_for

from src.app.resources.api import api


@api.route("/", methods=["GET"])
def index():
    return redirect(url_for("flasgger.apidocs"))
