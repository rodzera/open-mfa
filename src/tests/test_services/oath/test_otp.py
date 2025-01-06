from time import time
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from src.app.services.oath import OTPService
from src.app.services.oath import BaseOTPService
from src.app.repositories.oath import OTPRepository
from src.app.configs.oath import OTP_DF_CONFIG
from src.tests.utils import test_b64_cipher_secret, test_b32_secret


def test_service_type_attr() -> None:
    assert OTPService._service_type == "otp"

def test_repository_class_attr() -> None:
    assert OTPService._repository_class == OTPRepository

def test_df_config_attr() -> None:
    assert OTPService._df_config == OTP_DF_CONFIG

def test_init(mocker: MockerFixture) -> None:
    mock_get_session_data = mocker.patch.object(
        BaseOTPService,
        "_get_session_data",
        return_value={"secret": test_b64_cipher_secret, "otp": "654321"}
    )
    mock_otp = mocker.patch("src.app.services.oath.otp.OTP")
    server_data = {"otp": "123456"}

    service = OTPService(**server_data)

    assert service._used_otp == 0
    assert service._cached_otp == mock_get_session_data.return_value["otp"]
    assert service._current_timestamp == int(time())
    assert service._creation_timestamp == 0
    assert service._server_otp == mock_otp.return_value.generate_otp.return_value
    mock_otp.assert_called_once_with(test_b32_secret, digest=OTPService._hash_method)
    mock_otp.return_value.generate_otp.assert_called_once_with(
        service._current_timestamp
    )

def test_create_otp_not_cached() -> None:
    mock_self = MagicMock(_cached_otp=None)
    response = OTPService._create(mock_self)
    assert response["otp"] == mock_self._server_otp
    mock_self._insert_session_data.assert_called_once_with()

def test_create_otp_cached() -> None:
    mock_self = MagicMock()
    response = OTPService._create(mock_self)
    assert response["otp"] == mock_self._cached_otp

def test_create_otp_cached_but_not_valid() -> None:
    mock_self = MagicMock()
    mock_self._is_otp_valid.return_value = False

    response = OTPService._create(mock_self)

    assert response["otp"] == mock_self._server_otp
    mock_self._insert_session_data.assert_called_once_with()

def test_verify_success() -> None:
    mock_self = MagicMock(_client_otp="123456", _cached_otp="123456")
    mock_self._is_otp_valid.return_value = True

    response = OTPService._verify(mock_self)

    assert response["status"] is True
    mock_self._is_otp_valid.assert_called_once_with()
    mock_self._set_otp_as_used.assert_called_once_with()

def test_verify_wrong_otp() -> None:
    mock_self = MagicMock(_client_otp="123456", _cached_otp="654321")

    response = OTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._is_otp_valid.assert_not_called()
    mock_self._set_otp_as_used.assert_not_called()

def test_verify_otp_is_not_valid_anymore() -> None:
    mock_self = MagicMock(_client_otp="123456", _cached_otp="123456")
    mock_self._is_otp_valid.return_value = False

    response = OTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._is_otp_valid.assert_called_once_with()
    mock_self._set_otp_as_used.assert_not_called()

def test_redis_data(mocker: MockerFixture) -> None:
    mock_get_session_data = mocker.patch.object(
        BaseOTPService,
        "_get_session_data",
        return_value={"secret": test_b64_cipher_secret}
    )
    mock_otp = mocker.patch("src.app.services.oath.otp.OTP")
    server_data = {"otp": "123456"}
    service = OTPService(**server_data)
    default_data = service._redis_data

    assert default_data["otp"] == mock_otp.return_value.generate_otp.return_value
    assert default_data["secret"] == mock_get_session_data.return_value["secret"]
    assert default_data["used"] == 0
    assert default_data["timestamp"] == int(time())
    mock_otp.assert_called_once_with(test_b32_secret, digest=OTPService._hash_method)
    mock_otp.return_value.generate_otp.assert_called_once_with(
        service._current_timestamp
    )
    mock_get_session_data.assert_called_once_with()

def test_set_otp_as_used() -> None:
    mock_self = MagicMock()
    OTPService._set_otp_as_used(mock_self)
    mock_self._repository.set_otp_as_used.assert_called_once_with()

def test_otp_has_expired() -> None:
    mock_self = MagicMock(
        _df_config=OTP_DF_CONFIG,
        _current_timestamp=int(time()) + OTP_DF_CONFIG["expires_in"],
        _creation_timestamp=int(time())
    )
    response = OTPService._otp_has_expired(mock_self)
    assert response is True

def test_otp_has_not_expired() -> None:
    mock_self = MagicMock(
        _df_config=OTP_DF_CONFIG,
        _current_timestamp=int(time()),
        _creation_timestamp=int(time())
    )
    response = OTPService._otp_has_expired(mock_self)
    assert response is False

def test_is_otp_valid() -> None:
    mock_self = MagicMock(_used_otp=False)
    mock_self._otp_has_expired.return_value = False
    response = OTPService._is_otp_valid(mock_self)
    assert response is True

def test_is_otp_valid_already_used_otp() -> None:
    mock_self = MagicMock(_used_otp=True)
    mock_self._otp_has_expired.return_value = False
    response = OTPService._is_otp_valid(mock_self)
    assert response is False

def test_is_otp_valid_already_expired_otp() -> None:
    mock_self = MagicMock(_used_otp=False)
    mock_self._otp_has_expired.return_value = True
    response = OTPService._is_otp_valid(mock_self)
    assert response is False
