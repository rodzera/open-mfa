from unittest.mock import MagicMock
from flask.ctx import RequestContext
from pytest_mock import MockerFixture

from src.app.services.oath.totp import TOTPService
from src.tests.utils import test_b64_cipher_secret, test_b32_secret


def test_type_prop() -> None:
    assert TOTPService._service_type == "totp"

def test_init(
    redis_db: MagicMock, mocker: MockerFixture, req_ctx: RequestContext
) -> None:
    mock_get_session_key = mocker.patch.object(
        TOTPService, "_get_session_key", return_value="session_key"
    )
    mock_totp = mocker.patch("src.app.services.oath.totp.TOTP")
    redis_db.return_value = {
        "secret": test_b64_cipher_secret, "last_used_otp": "123456"
    }
    service_data = {"otp": "123456", "interval": 60}
    mock_session = mocker.patch("src.app.services.oath.totp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = TOTPService(**service_data)

    assert service._client_interval == service_data["interval"]
    assert service._last_used_otp == redis_db.return_value["last_used_otp"]
    assert service._server_totp == mock_totp.return_value
    assert service._totp_uri == mock_totp.return_value.provisioning_uri.return_value
    mock_totp.assert_called_once_with(
        test_b32_secret,
        interval=service_data["interval"],
        digest=TOTPService._hash_method
    )
    mock_totp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa"
    )
    mock_get_session_key.assert_called_once_with()

def test_create() -> None:
    mock_self = MagicMock()
    response = TOTPService._create(mock_self)
    assert response["uri"] == mock_self._totp_uri

def test_verify_success() -> None:
    mock_self = MagicMock(_client_otp="123456", _last_used_otp="654321")
    mock_self._server_totp.verify.return_value = True

    response = TOTPService._verify(mock_self)

    assert response["status"] is True
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._server_totp.verify.assert_called_once_with(
        mock_self._client_otp, valid_window=1
    )
    mock_self._set_last_used_otp.assert_called_once_with()

def test_verify_failure() -> None:
    mock_self = MagicMock(_client_otp="654321", _last_used_otp="654321")
    mock_self._server_totp.verify.return_value = False

    response = TOTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._server_totp.verify.assert_called_once_with(
        mock_self._client_otp, valid_window=1
    )
    mock_self._set_last_used_otp.assert_not_called()

def test_redis_data(
    redis_db: MagicMock, mocker: MockerFixture, req_ctx: RequestContext
)-> None:
    mock_get_session_key = mocker.patch.object(
        TOTPService, "_get_session_key", return_value="session_key"
    )
    mock_totp = mocker.patch("src.app.services.oath.totp.TOTP")
    redis_db.return_value = {"secret": test_b64_cipher_secret, "last_used_otp": "123456"}
    service_data = {"otp": "123456", "interval": 60}
    mock_session = mocker.patch("src.app.services.oath.totp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = TOTPService(**service_data)
    default_data = service._redis_data

    assert default_data["interval"] == service_data["interval"]
    assert default_data["secret"] == redis_db.return_value["secret"]
    assert default_data["uri"] == mock_totp.return_value.provisioning_uri.return_value
    assert default_data["last_used_otp"] == 0
    mock_totp.assert_called_once_with(
        test_b32_secret,
        interval=service_data["interval"],
        digest=TOTPService._hash_method
    )
    mock_totp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa"
    )
    mock_get_session_key.assert_called_once_with()

def test_set_last_used_otp(redis_db: MagicMock) -> None:
    mock_self = MagicMock(_cached_count=0)
    TOTPService._set_last_used_otp(mock_self)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"last_used_otp": mock_self._client_otp}
    )
