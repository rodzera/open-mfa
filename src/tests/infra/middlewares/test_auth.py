from flask import Flask
from typing import Dict
from _pytest.python_api import raises
from werkzeug.exceptions import Unauthorized

from src.tests.helpers import basic_auth
from src.app.infra.middlewares.auth import auth_middleware


@auth_middleware
def func() -> bool:
    return True

def test_valid_admin_auth(app: Flask, basic_admin_auth: Dict) -> None:
    with app.test_request_context("/", headers={**basic_admin_auth}):
        assert func() is True

def test_invalid_admin_auth_wrong_username(app: Flask) -> None:
    invalid_cred = basic_auth("wrong", "admin")
    with app.test_request_context("/", headers={**invalid_cred}):
        with raises(Unauthorized):
            func()

def test_invalid_admin_auth_wrong_password(app: Flask) -> None:
    invalid_cred = basic_auth("admin", "password")
    with app.test_request_context("/", headers={**invalid_cred}):
        with raises(Unauthorized):
            func()

def test_missing_admin_auth_missing_auth_in_headers(app: Flask) -> None:
    with app.test_request_context("/"):
        with raises(Unauthorized):
            func()
