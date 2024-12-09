from unittest.mock import MagicMock
from flask.ctx import RequestContext
from pytest_mock import MockerFixture

from src.app.services.mfa.hotp import HOTPService


def test_type_prop() -> None:
    assert HOTPService._service_type == "hotp"

def test_init(
    redis_db: MagicMock, mocker: MockerFixture, req_ctx: RequestContext
) -> None:
    mock_get_session_key = mocker.patch.object(
        HOTPService, "_get_session_key", return_value="session_key"
    )
    mock_hotp = mocker.patch("src.app.services.mfa.hotp.HOTP")
    redis_db.return_value = {"secret": "s3cr3t", "count": 1}
    service_data = {"otp": "123456", "initial_count": 10}
    mock_session = mocker.patch("src.app.services.mfa.hotp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = HOTPService(**service_data)

    assert service._client_initial_count == service_data["initial_count"]
    assert service._cached_count == 1
    assert service._server_hotp == mock_hotp.return_value
    assert service._hotp_uri == mock_hotp.return_value.provisioning_uri.return_value
    mock_hotp.assert_called_once_with(
        redis_db.return_value["secret"],
        initial_count=service_data["initial_count"]
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

def test_verify_success() -> None:
    mock_self = MagicMock(_cached_count=0)
    mock_self._server_hotp.verify.return_value = True

    response = HOTPService._verify(mock_self)

    assert response["status"] is True
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._server_hotp.verify.assert_called_once_with(
        mock_self._client_otp, mock_self._cached_count + 1
    )
    mock_self._increase_hotp_counter.assert_called_once_with()

def test_verify_failure() -> None:
    mock_self = MagicMock(_cached_count=0)
    mock_self._server_hotp.verify.return_value = False

    response = HOTPService._verify(mock_self)

    assert response["status"] is False
    mock_self._log_action.assert_called_once_with("verify")
    mock_self._server_hotp.verify.assert_called_once_with(
        mock_self._client_otp, mock_self._cached_count + 1
    )
    mock_self._increase_hotp_counter.assert_not_called()

def test_default_data(
    redis_db: MagicMock, mocker: MockerFixture, req_ctx: RequestContext
)-> None:
    mock_get_session_key = mocker.patch.object(
        HOTPService, "_get_session_key", return_value="session_key"
    )
    mock_hotp = mocker.patch("src.app.services.mfa.hotp.HOTP")
    redis_db.return_value = {"secret": "s3cr3t", "count": 1}
    service_data = {"otp": "123456", "initial_count": 10}
    mock_session = mocker.patch("src.app.services.mfa.hotp.session")
    mock_session.__getitem__.return_value = "session_key"

    service = HOTPService(**service_data)
    default_data = service._default_data

    assert default_data["count"] == service_data["initial_count"]
    assert default_data["secret"] == redis_db.return_value["secret"]
    assert default_data["uri"] == mock_hotp.return_value.provisioning_uri.return_value
    mock_hotp.assert_called_once_with(
        redis_db.return_value["secret"],
        initial_count=service_data["initial_count"]
    )
    mock_hotp.return_value.provisioning_uri.assert_called_once_with(
        name=mock_session.__getitem__.return_value, issuer_name="open-mfa",
        initial_count=service._client_initial_count
    )
    mock_get_session_key.assert_called_once_with()

def test_increase_hotp_counter(redis_db: MagicMock) -> None:
    mock_self = MagicMock(_cached_count=0)
    HOTPService._increase_hotp_counter(mock_self)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"count": mock_self._cached_count + 1}
    )
