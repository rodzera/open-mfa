from datetime import timedelta
from flask.ctx import RequestContext
from pytest_mock import MockerFixture
from unittest.mock import PropertyMock, MagicMock

from src.app.repositories.oath import BaseOTPRepository


def test_get_session_data(mocker: MockerFixture, mock_redis_db: MagicMock) -> None:
    mock_oath_session_key = mocker.patch.object(BaseOTPRepository, "_oath_session_key")
    service = BaseOTPRepository()
    data = service.get_session_data()

    assert data == mock_redis_db.return_value
    mock_redis_db.assert_called_once_with("hgetall", mock_oath_session_key)

def test_insert_session_data(mocker: MockerFixture, mock_redis_db: MagicMock) -> None:
    mock_oath_session_key = mocker.patch.object(BaseOTPRepository, "_oath_session_key")
    data = {}
    service = BaseOTPRepository()
    service.insert_session_data(data)

    mock_redis_db.assert_has_calls([
        mocker.call("hset", mock_oath_session_key, mapping=data),
        mocker.call("expire", mock_oath_session_key, timedelta(minutes=60))
    ])

def test_service_check_session_data_exists(
    mocker: MockerFixture, mock_redis_db: MagicMock
) -> None:
    mock_oath_session_key = mocker.patch.object(BaseOTPRepository, "_oath_session_key")
    service = BaseOTPRepository()
    data = service.check_session_data_exists()

    assert data == mock_redis_db.return_value
    mock_redis_db.assert_called_once_with("exists", mock_oath_session_key)

def test_service_delete_session_data(
    mocker: MockerFixture, mock_redis_db: MagicMock
) -> None:
    mock_oath_session_key = mocker.patch.object(BaseOTPRepository, "_oath_session_key")
    service = BaseOTPRepository()
    data = service.delete_session_data()

    assert data == mock_redis_db.return_value
    mock_redis_db.assert_called_once_with("delete", mock_oath_session_key)

def test_oath_session_key_prop(
    req_ctx: RequestContext, mocker: MockerFixture
) -> None:
    mock_service_type = mocker.patch.object(
        BaseOTPRepository,
        "_service_type",
        new_callable=PropertyMock,
        create=True
    )
    mock_service_type.return_value = "type"
    service = BaseOTPRepository()
    oath_key = service._oath_session_key

    assert BaseOTPRepository._user_session.manage_session() in oath_key
