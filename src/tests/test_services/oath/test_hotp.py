from flask.ctx import RequestContext
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, call

from src.app.services.oath import HOTPService
from src.app.services.oath import BaseOTPService
from src.app.repositories.oath import HOTPRepository
from src.app.configs.oath import HOTP_DF_CONFIG
from src.tests.utils import test_b64_cipher_secret, test_b32_secret


def test_service_type_attr() -> None:
    assert HOTPService._service_type == "hotp"

def test_repository_class_attr() -> None:
    assert HOTPService._repository_class == HOTPRepository

def test_df_config_attr() -> None:
    assert HOTPService._df_config == HOTP_DF_CONFIG

def test_init(mocker: MockerFixture, req_ctx: RequestContext) -> None:
    mock_get_session_data = mocker.patch.object(
        BaseOTPService,
        "_get_session_data",
        return_value={"secret": test_b64_cipher_secret, "count": 1}
    )
    mock_hotp = mocker.patch("src.app.services.oath.hotp.HOTP")
    server_data = {"otp": "123456", "initial_count": 10}
    mock_session = mocker.patch("src.app.services.oath.hotp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = HOTPService(**server_data)

    assert service._client_initial_count == server_data["initial_count"]
    assert service._cached_count == mock_get_session_data.return_value["count"]
    assert service._server_hotp == mock_hotp.return_value
    assert service._hotp_uri == mock_hotp.return_value.provisioning_uri.return_value
    mock_hotp.assert_called_once_with(
        test_b32_secret,
        initial_count=server_data["initial_count"],
        digest=HOTPService._hash_method
    )
    mock_hotp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa",
        initial_count=service._client_initial_count
    )

def test_create() -> None:
    mock_self = MagicMock()
    response = HOTPService._create(mock_self)
    assert response["uri"] == mock_self._hotp_uri

def test_verify_success_without_resync_protocol() -> None:
    mock_self = MagicMock(_cached_count=0)
    mock_self._server_hotp.verify.return_value = True

    response = HOTPService._verify(mock_self)

    assert response["status"] is True
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

def test_redis_data(mocker: MockerFixture, req_ctx: RequestContext) -> None:
    mock_get_session_data = mocker.patch.object(
        BaseOTPService,
        "_get_session_data",
        return_value={"secret": test_b64_cipher_secret, "count": 1}
    )
    mock_hotp = mocker.patch("src.app.services.oath.hotp.HOTP")
    server_data = {
        "otp": "123456", "initial_count": 10, "resync_threshold": 5
    }
    mock_session = mocker.patch("src.app.services.oath.hotp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = HOTPService(**server_data)
    default_data = service._redis_data

    assert default_data["count"] == server_data["initial_count"]
    assert default_data["secret"] == mock_get_session_data.return_value["secret"]
    assert default_data["uri"] == mock_hotp.return_value.provisioning_uri.return_value
    assert default_data["resync_threshold"] == server_data["resync_threshold"]
    mock_hotp.assert_called_once_with(
        test_b32_secret,
        initial_count=server_data["initial_count"],
        digest=HOTPService._hash_method
    )
    mock_hotp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa",
        initial_count=service._client_initial_count
    )

def test_increase_hotp_counter(mock_redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    counter = 0
    HOTPService._increase_hotp_counter(mock_self, counter)
    mock_self._repository.increase_hotp_counter.assert_called_once_with(counter)
