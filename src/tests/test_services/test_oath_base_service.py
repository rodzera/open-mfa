from abc import ABC
from hashlib import sha256
from unittest.mock import MagicMock
from _pytest.python_api import raises
from pytest_mock import MockerFixture

from src.app.services.oath import BaseOTPService
from src.app.infra.aes_cipher import AESCipherService
from src.tests.utils import test_b64_cipher_secret, test_cipher_secret, \
    test_b32_secret


def test_is_abc_sub_class() -> None:
    assert issubclass(BaseOTPService, ABC)

def test_default_hash_method() -> None:
    assert getattr(BaseOTPService, "_hash_method", sha256)

def test_init() -> None:
    mock_self, mock_repo = MagicMock(), MagicMock()
    BaseOTPService.__init__(mock_self, mock_repo, otp="123456")

    assert mock_self._repository == mock_repo.return_value
    assert mock_self._client_otp == "123456"
    assert mock_self._session_data == mock_self._get_session_data.return_value
    mock_self._setup_secrets.assert_called_once()

def test_get_session_data() -> None:
    mock_self = MagicMock()
    data = BaseOTPService._get_session_data(mock_self)
    assert data == mock_self._repository.get_session_data.return_value

def test_insert_session_data() -> None:
    mock_self = MagicMock()
    BaseOTPService._insert_session_data(mock_self)
    mock_self._repository.insert_session_data.assert_called_once_with(
        mock_self._redis_data
    )

def test_check_session_data_exists() -> None:
    mock_self = MagicMock()
    data = BaseOTPService._check_session_data_exists(mock_self)
    assert data == mock_self._repository.check_session_data_exists.return_value

def test_delete_session_data() -> None:
    mock_self = MagicMock()
    data = BaseOTPService._delete_session_data(mock_self)
    assert data == mock_self._repository.delete_session_data.return_value

def test_setup_secrets_method_with_session_data() -> None:
    server_data = {"secret": test_b64_cipher_secret}
    mock_self = MagicMock(_session_data=server_data)
    BaseOTPService._setup_secrets(mock_self)
    assert mock_self._b64_cipher_secret == server_data["secret"]
    assert mock_self._cipher_secret == test_cipher_secret
    assert mock_self._secret == test_b32_secret

def test_setup_secrets_method_missing_session_data(
    mocker: MockerFixture
) -> None:
    mock_random_base32 = mocker.patch(
        "src.app.services.oath.base_otp.random_base32",
        return_value=test_b32_secret
    )
    mock_encrypt = mocker.patch.object(
        AESCipherService, "encrypt", return_value=test_cipher_secret
    )
    mock_self = MagicMock(_session_data={})

    BaseOTPService._setup_secrets(mock_self)

    assert mock_self._secret == mock_random_base32.return_value
    assert mock_self._cipher_secret == test_cipher_secret
    assert mock_self._b64_cipher_secret == test_b64_cipher_secret
    mock_random_base32.assert_called_once()
    mock_encrypt.assert_called_once_with(mock_random_base32.return_value.encode())

def test_delete_data() -> None:
    mock_self = MagicMock(_service_type="totp", spec=BaseOTPService)

    BaseOTPService.delete_data(mock_self)
    mock_self._check_session_data_exists.assert_called_once_with()
    mock_self._delete_session_data.assert_called_once_with()

def test_delete_data_oath_session_key_does_not_exists() -> None:
    mock_self = MagicMock(_service_type="totp", spec=BaseOTPService)
    mock_self._check_session_data_exists.return_value = False

    status = BaseOTPService.delete_data(mock_self)

    assert status == 0
    mock_self._check_session_data_exists.assert_called_once_with()
    mock_self._delete_session_data.assert_not_called()

def test_delete_data_attribute_error() -> None:
    mock_self = MagicMock(_service_type="otp", spec=BaseOTPService)

    with raises(AttributeError):
        BaseOTPService.delete_data(mock_self)

def test_process_request_verify() -> None:
    mock_self = MagicMock(_client_otp="123456")

    BaseOTPService.process_request(mock_self)
    mock_self._verify.assert_called_once_with()

def test_process_request_create() -> None:
    mock_self = MagicMock(_client_otp=None)

    BaseOTPService.process_request(mock_self)
    mock_self._create.assert_called_once_with()

def test_has_abstract_methods() -> None:
    abstract_methods = BaseOTPService.__abstractmethods__
    assert "_redis_data" in abstract_methods
    assert "_verify" in abstract_methods
    assert "_create" in abstract_methods
