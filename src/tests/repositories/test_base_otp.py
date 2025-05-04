from datetime import timedelta
from flask.ctx import RequestContext
from pytest_mock import MockerFixture
from unittest.mock import PropertyMock, MagicMock

from src.app.repositories.oath import OTPRepository


def test_get_session_data(mocker: MockerFixture, mock_redis_db: MagicMock) -> None:
    mock_oath_session_key = mocker.patch.object(OTPRepository, "oath_session_key")
    service = OTPRepository(service_type="otp")
    data = service.get_session_data()

    assert data == mock_redis_db.return_value
    mock_redis_db.assert_called_once_with("hgetall", mock_oath_session_key)

def test_insert_session_data(mocker: MockerFixture, mock_redis_db: MagicMock) -> None:
    mock_oath_session_key = mocker.patch.object(OTPRepository, "oath_session_key")
    data = {}
    service = OTPRepository(service_type="otp")
    service.insert_session_data(data, exp=True)

    mock_redis_db.assert_has_calls([
        mocker.call("hset", mock_oath_session_key, mapping=data),
        mocker.call("expire", mock_oath_session_key, timedelta(minutes=60))
    ])

def test_service_session_data_exists(
    mocker: MockerFixture, mock_redis_db: MagicMock
) -> None:
    mock_oath_session_key = mocker.patch.object(OTPRepository, "oath_session_key")
    service = OTPRepository(service_type="otp")
    data = service.session_data_exists()

    assert data == mock_redis_db.return_value
    mock_redis_db.assert_called_once_with("exists", mock_oath_session_key)

def test_service_delete_session_data(
    mocker: MockerFixture, mock_redis_db: MagicMock
) -> None:
    mock_oath_session_key = mocker.patch.object(OTPRepository, "oath_session_key")
    service = OTPRepository(service_type="otp")
    data = service.delete_session_data()

    assert data == mock_redis_db.return_value
    mock_redis_db.assert_called_once_with("delete", mock_oath_session_key)

def test_oath_session_key_prop(req_ctx: RequestContext) -> None:
    service = OTPRepository(service_type="otp")
    oath_key = service.oath_session_key

    session_id = service.user_session.manage_session()
    assert oath_key == f"{session_id}:{service.service_type}"

def test_user_session_id_prop(req_ctx: RequestContext) -> None:
    service = OTPRepository(service_type="otp")
    assert service.user_session_id == service.user_session.manage_session()
