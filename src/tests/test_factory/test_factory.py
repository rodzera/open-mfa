from flask import Flask
from pytest_mock import MockerFixture

from src.app.factory import create_app


def test_create_app(mocker: MockerFixture) -> None:
    mock_ma = mocker.patch("src.app.factory.ma")
    mock_register_error_handlers = mocker.patch("src.app.factory.register_error_handlers")
    mock_register_gunicorn_signal_handler = mocker.patch("src.app.factory.register_gunicorn_signal_handler")

    app = create_app()
    assert isinstance(app, Flask)
    mock_ma.init_app.assert_called_once()
    mock_register_error_handlers.assert_called_once()
    mock_register_gunicorn_signal_handler.assert_called_once()
