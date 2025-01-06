import pytest
from typing import Optional
from pytest_mock import MockerFixture

from src.app.infra.aes_cipher import AESCipherService
from src.tests.utils import test_cipher_secret, test_b32_secret


@pytest.mark.parametrize(
    "env_value, expected_exception",
    [
        (None, SystemExit),
        ("invalid_base64", SystemExit),
        ("dGVzdC1rZXk=", SystemExit),  # "test-key" in b64
        ("QUJDREVGR0gxMjM0NTY3OA==", None)  # ABCDEFGH12345678 in b64
    ]
)

def test_parse_aes_key_from_environ(
    mocker: MockerFixture, cipher_service: AESCipherService,
    env_value: Optional[str], expected_exception: Optional[SystemExit],
):
    get_env = mocker.patch(
        "src.app.infra.aes_cipher.getenv", return_value=env_value
    )
    if expected_exception:
        with pytest.raises(expected_exception):
            cipher_service.parse_aes_key_from_environ()
    else:
        aes_key = cipher_service.parse_aes_key_from_environ()
        assert aes_key == b"ABCDEFGH12345678"

    get_env.assert_called_once_with("_B64_AES_KEY")


def test_generate_random_bytes(
    mocker: MockerFixture, cipher_service: AESCipherService
):
    mock_generate_random_bytes = mocker.patch.object(
        cipher_service, "generate_random_bytes",
        return_value=b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
    )
    random_bytes = cipher_service.generate_random_bytes(16)
    assert random_bytes == b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
    mock_generate_random_bytes.assert_called_once_with(16)


def test_encrypt(mocker: MockerFixture, cipher_service: AESCipherService):
    mock_generate_random_bytes = mocker.patch.object(
        cipher_service, "generate_random_bytes",
        return_value=b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
    )
    data = b"test_data"
    encrypted_data = cipher_service.encrypt(data)

    assert len(encrypted_data) == 16 + len(data) + 16
    assert encrypted_data.startswith(mock_generate_random_bytes.return_value)
    mock_generate_random_bytes.assert_called_once_with()


def test_decrypt(cipher_service: AESCipherService):
    decrypted_data = cipher_service.decrypt(test_cipher_secret)
    assert decrypted_data.decode() == test_b32_secret
