from typing import Dict
from unittest.mock import MagicMock
from flask.testing import FlaskClient

from src.tests.utils import json_accept_header, json_content_type_header


def test_get_logger_level_200(
    client: FlaskClient, redis_db: MagicMock, basic_admin_auth: Dict
) -> None:
    response = client.get(
        "/api/logs",
        headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["level"] == "INFO"

def test_set_logger_level_to_debug_200(
    client: FlaskClient, redis_db: MagicMock, basic_admin_auth: Dict
) -> None:
    response = client.put(
        "/api/logs", json={"level": "DEBUG"},
        headers={**json_content_type_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["level"] == "DEBUG"

def test_set_logger_level_to_notset_400(
    client: FlaskClient, redis_db: MagicMock, basic_admin_auth: Dict
) -> None:
    response = client.put(
        "/api/logs", json={"level": "NOTSET"},
        headers={**json_content_type_header(), **basic_admin_auth}
    )
    assert response.status_code == 400
    assert response.json["description"] == "Must be one of: CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG."
