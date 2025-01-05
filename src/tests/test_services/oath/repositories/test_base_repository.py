from pytest_mock import MockerFixture
from unittest.mock import PropertyMock

from src.app.services.oath.repositories import BaseOTPRepository


def test_get_session_data(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repositories.base_repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    service = BaseOTPRepository()
    data = service.get_session_data()

    assert data == mock_redis_service.db.return_value
    mock_redis_service.db.assert_called_once_with("hgetall", mock_session_key)

def test_create_session_data(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repositories.base_repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    data = {}
    service = BaseOTPRepository()
    service.create_session_data(data)

    mock_redis_service.insert_hset.assert_called_once_with(
        mock_session_key, data
    )

def test_service_verify_session_key_exists(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repositories.base_repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    service = BaseOTPRepository()
    data = service.verify_session_key_exists()

    assert data == mock_redis_service.db.return_value
    mock_redis_service.db.assert_called_once_with("exists", mock_session_key)

def test_service_delete_session_key(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repositories.base_repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    service = BaseOTPRepository()
    data = service.delete_session_key()

    assert data == mock_redis_service.db.return_value
    mock_redis_service.db.assert_called_once_with("delete", mock_session_key)

def test_session_key_prop(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repositories.base_repository.redis_service"
    )
    mock_service_type = mocker.patch.object(
        BaseOTPRepository,
        "_service_type",
        new_callable=PropertyMock,
        create=True
    )
    mock_service_type.return_value = "type"
    service = BaseOTPRepository()
    key = service._session_key

    assert key == mock_redis_service.get_session_key.return_value
    mock_redis_service.get_session_key.assert_called_once_with(
        mock_service_type.return_value
    )
