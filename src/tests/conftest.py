from flask import Flask
from pytest import fixture
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from flask.ctx import RequestContext
from flask.testing import FlaskClient

from src.run import application
from src.app.services.redis import RedisService


@fixture(autouse=True)
def app() -> Flask:
    with application.app_context():
        yield application

@fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@fixture
def redis_db(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(RedisService, "db")

@fixture
def req_ctx(app: Flask) -> RequestContext:
    with app.test_request_context() as req:
        yield req
