from flask.ctx import RequestContext
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, call

from src.app.services.oath.hotp import HOTPService
from src.tests.utils import test_b64_cipher_secret, test_b32_secret


def test_type_prop() -> None:
    assert HOTPService._service_type == "hotp"

def test_init(
    redis_db: MagicMock, mocker: MockerFixture, req_ctx: RequestContext
) -> None:
    mock_get_session_key = mocker.patch.object(
        HOTPService, "_get_session_key", return_value="session_key"
    )
    mock_hotp = mocker.patch("src.app.services.oath.hotp.HOTP")
    redis_db.return_value = {"secret": test_b64_cipher_secret, "count": 1}
    service_data = {"otp": "123456", "initial_count": 10}
    mock_session = mocker.patch("src.app.services.oath.hotp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = HOTPService(**service_data)

    assert service._client_initial_count == service_data["initial_count"]
    assert service._cached_count == 1
    assert service._server_hotp == mock_hotp.return_value
    assert service._hotp_uri == mock_hotp.return_value.provisioning_uri.return_value
    mock_hotp.assert_called_once_with(
        test_b32_secret,
        initial_count=service_data["initial_count"],
        digest=HOTPService._hash_method
    )
    mock_hotp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa",
        initial_count=service._client_initial_count
    )
    mock_get_session_key.assert_called_once_with()

def test_create() -> None:
    mock_self = MagicMock()
    response = HOTPService._create(mock_self)
    assert response["uri"] == mock_self._hotp_uri

def test_verify_success_without_resync_protocol() -> None:
    mock_self = MagicMock(_cached_count=0)
    mock_self._server_hotp.verify.return_value = True

    response = HOTPService._verify(mock_self)

    assert response["status"] is True
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._server_hotp.verify.assert_called_once_with(
        mock_self._client_otp, mock_self._cached_count
    )
    mock_self._increase_hotp_counter.assert_called_once_with(
        mock_self._cached_count
    )

def test_verify_failure() -> None:
    mock_self = MagicMock(_cached_count=0)
    mock_self._server_hotp.verify.return_value = False
    mock_self._trigger_resync_protocol.return_value = False, 0

    response = HOTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._server_hotp.verify.assert_called_once_with(
        mock_self._client_otp, mock_self._cached_count
    )
    mock_self._trigger_resync_protocol.assert_called_once_with()
    mock_self._increase_hotp_counter.assert_not_called()

def test_trigger_resync_protocol_success() -> None:
    mock_self = MagicMock(_cached_count=0, _resync_threshold=5)
    mock_self._server_hotp.verify.side_effect = [
        False, False, False, False, True
    ]

    status, counter = HOTPService._trigger_resync_protocol(mock_self)

    assert status is True
    assert counter == mock_self._cached_count + 5
    mock_self._server_hotp.verify.assert_has_calls(
        [
            call(mock_self._client_otp, 1),
            call(mock_self._client_otp, 2),
            call(mock_self._client_otp, 3),
            call(mock_self._client_otp, 4),
            call(mock_self._client_otp, 5)
        ]
    )

def test_trigger_resync_protocol_failure() -> None:
    mock_self = MagicMock(_cached_count=0, _resync_threshold=5)
    mock_self._server_hotp.verify.side_effect = [
        False, False, False, False, False
    ]

    status, counter = HOTPService._trigger_resync_protocol(mock_self)

    assert status is False
    assert counter == 0
    mock_self._server_hotp.verify.assert_has_calls(
        [
            call(mock_self._client_otp, 1),
            call(mock_self._client_otp, 2),
            call(mock_self._client_otp, 3),
            call(mock_self._client_otp, 4),
            call(mock_self._client_otp, 5)
        ]
    )

def test_redis_data(
    redis_db: MagicMock, mocker: MockerFixture, req_ctx: RequestContext
)-> None:
    mock_get_session_key = mocker.patch.object(
        HOTPService, "_get_session_key", return_value="session_key"
    )
    mock_hotp = mocker.patch("src.app.services.oath.hotp.HOTP")
    redis_db.return_value = {"secret": test_b64_cipher_secret, "count": 1}
    service_data = {
        "otp": "123456", "initial_count": 10, "resync_threshold": 5
    }
    mock_session = mocker.patch("src.app.services.oath.hotp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = HOTPService(**service_data)
    default_data = service._redis_data

    assert default_data["count"] == service_data["initial_count"]
    assert default_data["secret"] == redis_db.return_value["secret"]
    assert default_data["uri"] == mock_hotp.return_value.provisioning_uri.return_value
    assert default_data["resync_threshold"] == service_data["resync_threshold"]
    mock_hotp.assert_called_once_with(
        test_b32_secret,
        initial_count=service_data["initial_count"],
        digest=HOTPService._hash_method
    )
    mock_hotp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa",
        initial_count=service._client_initial_count
    )
    mock_get_session_key.assert_called_once_with()

def test_increase_hotp_counter(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    counter = 0
    HOTPService._increase_hotp_counter(mock_self, counter)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"count": counter + 1}
    )
