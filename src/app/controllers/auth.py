from flask import current_app
from werkzeug.datastructures import Authorization


def authenticate_super_admin(auth: Authorization) -> bool:
    valid_user = auth.username == current_app.config["ADMIN_USER"]
    valid_pass = auth.password == current_app.config["ADMIN_PASS"]
    return valid_user and valid_pass
