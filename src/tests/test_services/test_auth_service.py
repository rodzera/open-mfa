from flask import Flask
from werkzeug.exceptions import Unauthorized

from src.app.services import admin_auth
from src.tests.utils import basic_admin_auth, basic_auth, test_case


@admin_auth()
def func() -> bool:
    return True

def test_valid_admin_auth(app: Flask) -> None:
    with app.test_request_context("/", headers={**basic_admin_auth}):
        assert func() is True

def test_invalid_admin_auth_wrong_username(app: Flask) -> None:
    invalid_cred = basic_auth("wrong", "admin")
    with app.test_request_context("/", headers={**invalid_cred}):
        with test_case.assertRaises(Unauthorized):
            func()

def test_invalid_admin_auth_wrong_password(app: Flask) -> None:
    invalid_cred = basic_auth("admin", "password")
    with app.test_request_context("/", headers={**invalid_cred}):
        with test_case.assertRaises(Unauthorized):
            func()

def test_missing_admin_auth_missing_auth_in_headers(app: Flask) -> None:
    with app.test_request_context("/"):
        with test_case.assertRaises(Unauthorized):
            func()
