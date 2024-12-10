from typing import Dict
from base64 import b64encode
from unittest import TestCase


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

basic_admin_auth = basic_auth("admin", "admin")
helper_test_case = TestCase()
