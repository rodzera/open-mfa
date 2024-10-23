from flask import redirect, url_for

from src.app.resources.views import views


@views.route("/", methods=["GET"])
def index():
    return redirect(url_for("flasgger.apidocs"))
