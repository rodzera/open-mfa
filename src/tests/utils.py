from typing import Dict
from base64 import b64encode
from pyotp import random_base32

from src.app.infra.aes_cipher import aes_cipher_service


def json_accept_header() -> Dict:
    return {"Accept": "application/json"}

def json_content_type_header() -> Dict:
    return {
        "Content-Type": "application/json",
        **json_accept_header()
    }

def basic_auth(username: str, password: str) -> Dict:
    credentials = f"{username}:{password}".encode()
    encoded_credentials = b64encode(credentials).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

test_b32_secret = random_base32()
test_cipher_secret = aes_cipher_service.encrypt(test_b32_secret.encode())
test_b64_cipher_secret = b64encode(test_cipher_secret).decode()
test_bytes = aes_cipher_service.generate_random_bytes()
