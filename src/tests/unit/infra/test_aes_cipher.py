import pytest
from typing import Optional
from pytest_mock import MockerFixture
from cryptography.exceptions import InvalidTag
from hypothesis import given, strategies as st, settings, HealthCheck

from src.tests.helpers import test_bytes
from src.infra.aes_cipher import AESCipherInfra


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
    mocker: MockerFixture, cipher_service: AESCipherInfra,
    env_value: Optional[str], expected_exception: Optional[SystemExit],
) -> None:
    get_env = mocker.patch(
        "src.infra.aes_cipher.getenv", return_value=env_value
    )
    if expected_exception:
        with pytest.raises(expected_exception):
            cipher_service.parse_aes_key_from_environ()
    else:
        aes_key = cipher_service.parse_aes_key_from_environ()
        assert aes_key == b"ABCDEFGH12345678"

    get_env.assert_called_once_with("_B64_AES_KEY")


def test_generate_random_bytes(
    mocker: MockerFixture, cipher_service: AESCipherInfra
) -> None:
    mock_generate_random_bytes = mocker.patch.object(
        cipher_service, "generate_random_bytes",
        return_value=test_bytes
    )
    random_bytes = cipher_service.generate_random_bytes(16)
    assert random_bytes == test_bytes
    mock_generate_random_bytes.assert_called_once_with(16)


@given(data=st.binary(min_size=1, max_size=1024))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_encrypt_properties(
    cipher_service: AESCipherInfra, mocker: MockerFixture, data: bytes
) -> None:
    mocked_iv = test_bytes
    mocker.patch.object(cipher_service, "generate_random_bytes", return_value=mocked_iv)

    encrypted_data = cipher_service.encrypt(data)

    expected_length = 16
    assert len(encrypted_data) == expected_length + len(data) + expected_length
    assert encrypted_data.startswith(mocked_iv)

    iv, ciphertext, tag = encrypted_data[:16], encrypted_data[16:-16], encrypted_data[-16:]
    assert iv == mocked_iv
    assert len(tag) == expected_length


@given(data=st.binary(min_size=1, max_size=1024))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_encrypt_decrypt_consistency(
    cipher_service: AESCipherInfra, data: bytes
) -> None:
    encrypted_data = cipher_service.encrypt(data)
    decrypted_data = cipher_service.decrypt(encrypted_data)
    assert decrypted_data == data


def test_encrypt_unique_iv(cipher_service: AESCipherInfra) -> None:
    data1, data2 = b"test_data_1", b"test_data_2"

    encrypted1 = cipher_service.encrypt(data1)
    encrypted2 = cipher_service.encrypt(data2)

    iv1, iv2 = encrypted1[:16], encrypted2[:16]
    assert iv1 != iv2


def test_decrypt_tampered_ciphertext(cipher_service: AESCipherInfra) -> None:
    iv = cipher_service.generate_random_bytes(16)
    ciphertext = b"tampered_ciphertext"
    tag = cipher_service.generate_random_bytes(16)
    tampered_data = iv + ciphertext + tag

    with pytest.raises(InvalidTag):
        cipher_service.decrypt(tampered_data)
