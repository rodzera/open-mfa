from _pytest.python_api import raises
from pytest_mock import MockerFixture
from unittest.mock import PropertyMock, MagicMock

from src.app.services.aes_cipher import AESCipherService
from src.app.services.mfa.base import RedisOTPHelperService, BaseOTPService
from src.tests.utils import test_b64_cipher_secret, test_cipher_secret, \
    test_b32_secret


def test_redis_otp_helper_service_get_session_key_method(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.mfa.base.redis_service"
    )

    service = RedisOTPHelperService()
    service._service_type = "type"
    service._get_session_key()

    mock_redis_service.get_session_key.assert_called_once_with(
        service._service_type
    )

def test_redis_otp_helper_service_verify_session_key_exists(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.mfa.base.redis_service"
    )

    service = RedisOTPHelperService()
    service._session_key = "session_key"
    service._verify_session_key_exists()

    mock_redis_service.db.assert_called_once_with(
        "exists", service._session_key
    )

def test_redis_otp_helper_service_delete_session_key(
    mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.mfa.base.redis_service"
    )

    service = RedisOTPHelperService()
    service._session_key = "session_key"
    service._delete_session_key()

    mock_redis_service.db.assert_called_once_with(
        "delete", service._session_key
    )

def test_base_otp_has_session_key_attr() -> None:
    assert hasattr(BaseOTPService, "_session_key")


def test_base_otp_service_init(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.mfa.base.redis_service", return_value={}
    )
    mock_get_session_key = mocker.patch.object(
        BaseOTPService, "_get_session_key"
    )
    mock_setup_secrets = mocker.patch.object(
        BaseOTPService, "_setup_secrets"
    )
    mock_redis_service.db.return_value = {}
    service = BaseOTPService(otp="123456")

    assert service._client_otp == "123456"
    mock_get_session_key.assert_called_once()
    mock_redis_service.db.assert_called_once_with(
        "hgetall", service._session_key
    )
    mock_setup_secrets.assert_called_once()

def test_base_otp_setup_secrets_method_with_service_data() -> None:
    service_data = {"secret": test_b64_cipher_secret}
    mock_self = MagicMock(_service_data=service_data)
    BaseOTPService._setup_secrets(mock_self)
    assert mock_self._b64_cipher_secret == service_data["secret"]
    assert mock_self._cipher_secret == test_cipher_secret
    assert mock_self._secret == test_b32_secret

def test_base_otp_setup_secrets_method_missing_service_data(
    mocker: MockerFixture
) -> None:
    mock_random_base32 = mocker.patch(
        "src.app.services.mfa.base.random_base32",
        return_value=test_b32_secret
    )
    mock_encrypt = mocker.patch.object(
        AESCipherService, "encrypt", return_value=test_cipher_secret
    )
    mock_self = MagicMock(_service_data={})

    BaseOTPService._setup_secrets(mock_self)

    assert mock_self._secret == mock_random_base32.return_value
    assert mock_self._cipher_secret == test_cipher_secret
    assert mock_self._b64_cipher_secret == test_b64_cipher_secret
    mock_random_base32.assert_called_once()
    mock_encrypt.assert_called_once_with(mock_random_base32.return_value.encode())

def test_base_otp_service_create_data(mocker: MockerFixture) -> None:
    mock_redis_service = mocker.patch(
        "src.app.services.mfa.base.redis_service"
    )
    mock_redis_service.db.return_value = {}
    mock_get_session_key = mocker.patch.object(
        BaseOTPService, "_get_session_key"
    )
    mock_redis_data = mocker.patch.object(
        BaseOTPService, "_redis_data", new_callable=PropertyMock, create=True
    )

    mock_get_session_key.return_value = "session_key"
    service = BaseOTPService(otp="123456")
    service._create_data()

    mock_redis_service.insert_hset.assert_called_once_with(
        mock_get_session_key.return_value, mock_redis_data.return_value
    )

def test_base_otp_service_delete_data() -> None:
    mock_self = MagicMock(_service_type="totp", spec=BaseOTPService)

    BaseOTPService.delete_data(mock_self)
    mock_self._log_action.assert_called_once_with("delete")
    mock_self._verify_session_key_exists.assert_called_once_with()
    mock_self._delete_session_key.assert_called_once_with()

def test_base_otp_service_delete_data_session_key_does_not_exists() -> None:
    mock_self = MagicMock(_service_type="totp", spec=BaseOTPService)
    mock_self._verify_session_key_exists.return_value = False

    status = BaseOTPService.delete_data(mock_self)

    assert status == 0
    mock_self._log_action.assert_called_once_with("delete")
    mock_self._verify_session_key_exists.assert_called_once_with()
    mock_self._delete_session_key.assert_not_called()

def test_base_otp_service_delete_data_attribute_error() -> None:
    mock_self = MagicMock(_service_type="otp", spec=BaseOTPService)

    with raises(AttributeError):
        BaseOTPService.delete_data(mock_self)

def test_base_otp_service_process_request_verify() -> None:
    mock_self = MagicMock(_client_otp="123456")

    BaseOTPService.process_request(mock_self)
    mock_self._verify.assert_called_once_with()

def test_base_otp_service_process_request_create() -> None:
    mock_self = MagicMock(_client_otp=None)

    BaseOTPService.process_request(mock_self)
    mock_self._create.assert_called_once_with()
