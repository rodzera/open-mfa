from typing import Dict
from base64 import b64encode


def headers(**kwargs) -> Dict:
    return {
        "Accept": "application/json",
        **kwargs
    }


def basic_auth(username: str, password: str) -> Dict:
    credentials = f"{username}:{password}".encode()
    encoded_credentials = b64encode(credentials).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}


payload = {"test": "test"}
admin_auth = basic_auth("admin", "admin")
