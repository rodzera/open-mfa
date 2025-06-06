from unittest.mock import MagicMock
from flask.testing import FlaskClient
from pytest_mock import MockerFixture


def test_verify_request_200(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_totp_service = mocker.patch("src.app.resources.api.oath.totp.TOTPService")
    mock_totp_service.return_value.get.return_value = {}

    req_params = {"otp": "123456", "interval": 30}
    response = client.get("/api/totp", query_string=req_params)

    assert response.status_code == 200
    assert response.json == {}
    mock_totp_service.assert_called_once_with(**req_params)
    mock_totp_service.return_value.get.assert_called_once_with()

def test_verify_request_404(
    client: FlaskClient, mocker: MockerFixture
) -> None:
    mock_totp_service = mocker.patch("src.app.resources.api.oath.totp.TOTPService")
    mock_totp_service.return_value.get.return_value = {}

    req_params = {"otp": "123456"}
    response = client.get("/api/totp", query_string=req_params)

    assert response.status_code == 404
    assert response.json["description"] == "TOTP not created"
    mock_totp_service.assert_not_called()
    mock_totp_service.return_value.get.assert_not_called()

def test_create_request_200(
    client: FlaskClient, mocker: MockerFixture
) -> None:
    mock_totp_service = mocker.patch("src.app.resources.api.oath.totp.TOTPService")
    mock_totp_service.return_value.get.return_value = {}

    req_params = {"interval": 30}
    response = client.get("/api/totp", query_string=req_params)

    assert response.status_code == 200
    assert response.json == {}
    mock_totp_service.assert_called_once_with(**req_params)
    mock_totp_service.return_value.get.assert_called_once_with()

def test_create_request_409(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_totp_service = mocker.patch("src.app.resources.api.oath.totp.TOTPService")
    mock_totp_service.return_value.get.return_value = {}

    req_params = {"interval": 30}
    response = client.get("/api/totp", query_string=req_params)

    assert response.status_code == 409
    assert response.json["description"] == "TOTP already created"
    mock_totp_service.assert_not_called()
    mock_totp_service.return_value.get.assert_not_called()

def test_delete_request_204(
    client: FlaskClient, mocker: MockerFixture
) -> None:
    mock_totp_service = mocker.patch("src.app.resources.api.oath.totp.TOTPService")
    mock_totp_service.return_value.delete.return_value = 1

    response = client.delete("/api/totp")

    assert response.status_code == 204
    mock_totp_service.assert_called_once_with()
    mock_totp_service.return_value.delete.assert_called_once_with()

def test_delete_request_404(
    client: FlaskClient, mocker: MockerFixture
) -> None:
    mock_totp_service = mocker.patch("src.app.resources.api.oath.totp.TOTPService")
    mock_totp_service.return_value.delete.return_value = 0

    response = client.delete("/api/totp")

    assert response.status_code == 404
    assert response.json["description"] == "TOTP not created"
    mock_totp_service.assert_called_once_with()
    mock_totp_service.return_value.delete.assert_called_once_with()
