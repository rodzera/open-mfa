from unittest.mock import MagicMock
from flask.testing import FlaskClient
from pytest_mock import MockerFixture


def test_verify_request_200(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_hotp_service = mocker.patch("src.app.resources.api.oath.hotp.HOTPService")
    mock_hotp_service.return_value.process_request.return_value = {}

    req_params = {"otp": "123456"}
    response = client.get("/api/hotp", query_string=req_params)

    assert response.status_code == 200
    assert response.json == {}
    mock_hotp_service.assert_called_once_with(**req_params)
    mock_hotp_service.return_value.process_request.assert_called_once_with()

def test_verify_request_404(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_hotp_service = mocker.patch("src.app.resources.api.oath.hotp.HOTPService")
    mock_hotp_service.return_value.process_request.return_value = {}
    mock_redis_db.return_value = None

    req_params = {"otp": "123456"}
    response = client.get("/api/hotp", query_string=req_params)

    assert response.status_code == 404
    assert response.json["description"] == "HOTP not created"
    mock_hotp_service.assert_not_called()
    mock_hotp_service.return_value.process_request.assert_not_called()

def test_create_request_200(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_hotp_service = mocker.patch("src.app.resources.api.oath.hotp.HOTPService")
    mock_hotp_service.return_value.process_request.return_value = {}
    mock_redis_db.return_value = None

    req_params = {"initial_count": 0}
    response = client.get("/api/hotp", query_string=req_params)

    assert response.status_code == 200
    assert response.json == {}
    mock_hotp_service.assert_called_once_with(**req_params)
    mock_hotp_service.return_value.process_request.assert_called_once_with()

def test_create_request_409(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_hotp_service = mocker.patch("src.app.resources.api.oath.hotp.HOTPService")
    mock_hotp_service.return_value.process_request.return_value = {}

    req_params = {"initial_count": 0}
    response = client.get("/api/hotp", query_string=req_params)

    assert response.status_code == 409
    assert response.json["description"] == "HOTP already created"
    mock_hotp_service.assert_not_called()
    mock_hotp_service.return_value.process_request.assert_not_called()

def test_delete_request_204(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_hotp_service = mocker.patch("src.app.resources.api.oath.hotp.HOTPService")
    mock_hotp_service.return_value.delete_data.return_value = 1

    response = client.delete("/api/hotp")

    assert response.status_code == 204
    mock_hotp_service.assert_called_once_with()
    mock_hotp_service.return_value.delete_data.assert_called_once_with()

def test_delete_request_404(
    client: FlaskClient, mock_redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_hotp_service = mocker.patch("src.app.resources.api.oath.hotp.HOTPService")
    mock_hotp_service.return_value.delete_data.return_value = 0

    response = client.delete("/api/hotp")

    assert response.status_code == 404
    assert response.json["description"] == "HOTP not created"
    mock_hotp_service.assert_called_once_with()
    mock_hotp_service.return_value.delete_data.assert_called_once_with()
