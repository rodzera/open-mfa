from pytest_mock import MockerFixture
from unittest.mock import PropertyMock, MagicMock

from src.app.services.oath.repository import OTPRepository, TOTPRepository, \
    HOTPRepository, BaseOTPRepository


def test_base_otp_repository_get_server_data(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    service = BaseOTPRepository()
    data = service.get_server_data()

    assert data == mock_redis_service.db.return_value
    mock_redis_service.db.assert_called_once_with("hgetall", mock_session_key)

def test_base_otp_repository_create_server_data(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    data = {}
    service = BaseOTPRepository()
    service.create_server_data(data)

    mock_redis_service.insert_hset.assert_called_once_with(
        mock_session_key, data
    )

def test_base_otp_repository_service_verify_session_key_exists(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    service = BaseOTPRepository()
    data = service.verify_session_key_exists()

    assert data == mock_redis_service.db.return_value
    mock_redis_service.db.assert_called_once_with("exists", mock_session_key)

def test_base_otp_repository_service_delete_session_key(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repository.redis_service"
    )
    mock_session_key = mocker.patch.object(BaseOTPRepository, "_session_key")
    service = BaseOTPRepository()
    data = service.delete_session_key()

    assert data == mock_redis_service.db.return_value
    mock_redis_service.db.assert_called_once_with("delete", mock_session_key)

def test_base_otp_repository_session_key_prop(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.oath.repository.redis_service"
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

def test_otp_repository_service_type_attr():
    assert OTPRepository._service_type == "otp"

def test_otp_repository_set_otp_as_used(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    OTPRepository.set_otp_as_used(mock_self)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key, mapping={"used": 1}
    )

def test_totp_repository_service_type_attr():
    assert TOTPRepository._service_type == "totp"

def test_totp_repository_set_last_used_otp(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    client_otp = "123456"
    TOTPRepository.set_last_used_otp(mock_self, client_otp)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"last_used_otp": client_otp}
    )

def test_hotp_repository_service_type_attr():
    assert HOTPRepository._service_type == "hotp"

def test_hotp_repository_increase_hotp_counter(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    counter = 0
    HOTPRepository.increase_hotp_counter(mock_self, counter)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"count": counter + 1}
    )
