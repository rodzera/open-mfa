from unittest.mock import MagicMock
from flask.ctx import RequestContext
from pytest_mock import MockerFixture

from src.app.services.oath.services.totp_service import TOTPService
from src.app.services.oath.services.base_service import BaseOTPService
from src.app.services.oath.repositories import TOTPRepository
from src.app.configs.oath import TOTP_DF_CONFIG
from src.tests.utils import test_b64_cipher_secret, test_b32_secret


def test_service_type_attr() -> None:
    assert TOTPService._service_type == "totp"

def test_repository_class_attr() -> None:
    assert TOTPService._repository_class == TOTPRepository

def test_df_config_attr() -> None:
    assert TOTPService._df_config == TOTP_DF_CONFIG

def test_init(mocker: MockerFixture, req_ctx: RequestContext) -> None:
    mock_get_server_data = mocker.patch.object(
        BaseOTPService,
        "_get_server_data",
        return_value={
            "secret": test_b64_cipher_secret, "last_used_otp": "123456"
        }
    )
    mock_totp = mocker.patch("src.app.services.oath.services.totp_service.TOTP")
    server_data = {"otp": "123456", "interval": 60}
    mock_session = mocker.patch("src.app.services.oath.services.totp_service.session")
    mock_session.__getitem__.return_value = "session_key"

    service = TOTPService(**server_data)

    assert service._client_interval == server_data["interval"]
    assert service._last_used_otp == mock_get_server_data.return_value["last_used_otp"]
    assert service._server_totp == mock_totp.return_value
    assert service._totp_uri == mock_totp.return_value.provisioning_uri.return_value
    mock_totp.assert_called_once_with(
        test_b32_secret,
        interval=server_data["interval"],
        digest=TOTPService._hash_method
    )
    mock_totp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa"
    )

def test_create() -> None:
    mock_self = MagicMock()
    response = TOTPService._create(mock_self)
    assert response["uri"] == mock_self._totp_uri

def test_verify_success() -> None:
    mock_self = MagicMock(_client_otp="123456", _last_used_otp="654321")
    mock_self._server_totp.verify.return_value = True

    response = TOTPService._verify(mock_self)

    assert response["status"] is True
    mock_self._server_totp.verify.assert_called_once_with(
        mock_self._client_otp, valid_window=mock_self._valid_window
    )
    mock_self._set_last_used_otp.assert_called_once_with()

def test_verify_failure() -> None:
    mock_self = MagicMock(_client_otp="654321", _last_used_otp="654321")
    mock_self._server_totp.verify.return_value = False

    response = TOTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._server_totp.verify.assert_called_once_with(
        mock_self._client_otp, valid_window=mock_self._valid_window
    )
    mock_self._set_last_used_otp.assert_not_called()

def test_redis_data(mocker: MockerFixture, req_ctx: RequestContext)-> None:
    mock_get_server_data = mocker.patch.object(
        BaseOTPService,
        "_get_server_data",
        return_value={
            "secret": test_b64_cipher_secret, "last_used_otp": "123456"
        }
    )
    mock_totp = mocker.patch("src.app.services.oath.services.totp_service.TOTP")
    server_data = {"otp": "123456", "interval": 60}
    mock_session = mocker.patch("src.app.services.oath.services.totp_service.session")
    mock_session.__getitem__.return_value = "session_key"

    service = TOTPService(**server_data)
    default_data = service._redis_data

    assert default_data["interval"] == server_data["interval"]
    assert default_data["secret"] == mock_get_server_data.return_value["secret"]
    assert default_data["uri"] == mock_totp.return_value.provisioning_uri.return_value
    assert default_data["last_used_otp"] == 0
    mock_totp.assert_called_once_with(
        test_b32_secret,
        interval=server_data["interval"],
        digest=TOTPService._hash_method
    )
    mock_totp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa"
    )

def test_set_last_used_otp() -> None:
    mock_self = MagicMock()
    TOTPService._set_last_used_otp(mock_self)
    mock_self._repository.set_last_used_otp.assert_called_once_with(
        mock_self._client_otp
    )
