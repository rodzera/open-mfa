from typing import Dict
from flask import Flask
from pytest import fixture
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from flask.ctx import RequestContext
from flask.testing import FlaskClient

from src.run import application
from src.tests.helpers import basic_auth
from src.infra.aes_cipher import aes_cipher_infra
from src.infra.redis import RedisInfra, redis_infra


@fixture(autouse=True)
def app() -> Flask:
    with application.app_context():
        yield application

@fixture(autouse=True)
def reset_fake_redis() -> None:
    redis_infra.client.flushdb()

@fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@fixture
def mock_redis_db(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(RedisInfra, "db")

@fixture
def req_ctx(app: Flask) -> RequestContext:
    with app.test_request_context() as req:
        yield req

@fixture
def basic_admin_auth() -> Dict:
    return basic_auth("admin", "admin")

@fixture
def cipher_service():
    return aes_cipher_infra
