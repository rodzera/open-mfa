from pytest import fixture

from src.run import application


@fixture(autouse=True)
def app():
    with application.app_context():
        yield application


@fixture
def client(app):
    return app.test_client()


@fixture
def req_ctx(app):
    with app.test_request_context() as req:
        yield req
