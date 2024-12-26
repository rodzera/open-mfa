from time import time
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from src.app.services.mfa.otp import OTPService
from src.tests.utils import test_b64_cipher_secret, test_b32_secret


def test_type_prop() -> None:
    assert OTPService._service_type == "otp"

def test_init(redis_db: MagicMock, mocker: MockerFixture) -> None:
    mock_get_session_key = mocker.patch.object(
        OTPService, "_get_session_key", return_value="session_key"
    )
    mock_otp = mocker.patch("src.app.services.mfa.otp.OTP")
    redis_db.return_value = {"secret": test_b64_cipher_secret}
    service_data = {"otp": "123456"}

    service = OTPService(**service_data)

    assert service._current_timestamp == int(time())
    assert service._creation_timestamp == 0
    assert service._used_otp == 0
    assert service._server_otp == mock_otp.return_value.generate_otp.return_value
    mock_otp.assert_called_once_with(test_b32_secret, digest=OTPService._hash_method)
    mock_otp.return_value.generate_otp.assert_called_once_with(
        service._current_timestamp
    )
    mock_get_session_key.assert_called_once_with()

def test_create_otp_not_cached() -> None:
    mock_self = MagicMock(_cached_otp=None)

    response = OTPService._create(mock_self)

    assert response["otp"] == mock_self._server_otp
    mock_self._log_action.assert_called_once_with("create")
    mock_self._create_data.assert_called_once_with()

def test_create_otp_cached() -> None:
    mock_self = MagicMock()

    response = OTPService._create(mock_self)

    assert response["otp"] == mock_self._cached_otp
    mock_self._log_action.assert_called_once_with("create")

def test_create_otp_cached_but_not_valid() -> None:
    mock_self = MagicMock()
    mock_self._is_otp_valid.return_value = False

    response = OTPService._create(mock_self)

    assert response["otp"] == mock_self._server_otp
    mock_self._log_action.assert_called_once_with("create")
    mock_self._create_data.assert_called_once_with()

def test_verify_success() -> None:
    mock_self = MagicMock(_client_otp="123456", _cached_otp="123456")
    mock_self._is_otp_valid.return_value = True

    response = OTPService._verify(mock_self)

    assert response["status"] is True
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._is_otp_valid.assert_called_once_with()
    mock_self._set_otp_as_used.assert_called_once_with()

def test_verify_wrong_otp() -> None:
    mock_self = MagicMock(_client_otp="123456", _cached_otp="654321")

    response = OTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._is_otp_valid.assert_not_called()
    mock_self._set_otp_as_used.assert_not_called()

def test_verify_otp_is_not_valid_anymore() -> None:
    mock_self = MagicMock(_client_otp="123456", _cached_otp="123456")
    mock_self._is_otp_valid.return_value = False

    response = OTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._is_otp_valid.assert_called_once_with()
    mock_self._set_otp_as_used.assert_not_called()

def test_redis_data(redis_db: MagicMock, mocker: MockerFixture) -> None:
    mock_get_session_key = mocker.patch.object(
        OTPService, "_get_session_key", return_value="session_key"
    )
    mock_otp = mocker.patch("src.app.services.mfa.otp.OTP")
    redis_db.return_value = {"secret": test_b64_cipher_secret}
    service_data = {"otp": "123456"}
    service = OTPService(**service_data)
    default_data = service._redis_data

    assert default_data["otp"] == mock_otp.return_value.generate_otp.return_value
    assert default_data["secret"] == redis_db.return_value["secret"]
    assert default_data["used"] == 0
    assert default_data["timestamp"] == int(time())
    mock_otp.assert_called_once_with(test_b32_secret, digest=OTPService._hash_method)
    mock_otp.return_value.generate_otp.assert_called_once_with(
        service._current_timestamp
    )
    mock_get_session_key.assert_called_once_with()

def test_set_otp_as_used(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    OTPService._set_otp_as_used(mock_self)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key, mapping={"used": 1}
    )

def test_otp_has_expired(redis_db: MagicMock) -> None:
    mock_self = MagicMock(
        _current_timestamp=int(time()) + 300,
        _creation_timestamp=int(time())
    )
    response = OTPService._otp_has_expired(mock_self)
    assert response is True

def test_otp_has_not_expired(redis_db: MagicMock) -> None:
    mock_self = MagicMock(
        _current_timestamp=int(time()),
        _creation_timestamp=int(time())
    )
    response = OTPService._otp_has_expired(mock_self)
    assert response is False

def test_is_otp_valid(redis_db: MagicMock) -> None:
    mock_self = MagicMock(
        _used_otp=False,
        _current_timestamp=int(time()),
        _creation_timestamp=int(time()) - 300
    )
    response = OTPService._otp_has_expired(mock_self)
    assert response is True

def test_is_otp_valid_not_valid_anymore(redis_db: MagicMock) -> None:
    mock_self = MagicMock(
        _used_otp=True,
        _current_timestamp=int(time()),
        _creation_timestamp=int(time())
    )
    response = OTPService._otp_has_expired(mock_self)
    assert response is False
