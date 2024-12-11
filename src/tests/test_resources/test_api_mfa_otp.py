from unittest.mock import MagicMock
from flask.testing import FlaskClient
from pytest_mock import MockerFixture


def test_verify_request_200(
    client: FlaskClient, redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_otp_service = mocker.patch("src.app.resources.api.mfa.otp.OTPService")
    mock_otp_service.return_value.process_request.return_value = {}

    req_params = {"otp": "123456"}
    response = client.get("/api/otp", query_string=req_params)

    assert response.status_code == 200
    assert response.json == {}
    mock_otp_service.assert_called_once_with(**req_params)
    mock_otp_service.return_value.process_request.assert_called_once_with()


def test_create_request_200(
    client: FlaskClient, redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_otp_service = mocker.patch("src.app.resources.api.mfa.otp.OTPService")
    mock_otp_service.return_value.process_request.return_value = {}

    response = client.get("/api/otp")

    assert response.status_code == 200
    assert response.json == {}
    mock_otp_service.assert_called_once_with()
    mock_otp_service.return_value.process_request.assert_called_once_with()
