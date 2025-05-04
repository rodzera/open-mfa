from typing import Dict
from logging import DEBUG, INFO
from flask.testing import FlaskClient

from src.app.repositories.logging import LoggingRepository
from src.tests.utils import json_accept_header, json_content_type_header


def test_get_logging_level_200(
    client: FlaskClient, basic_admin_auth: Dict
) -> None:
    LoggingRepository().set_level(INFO)
    response = client.get(
        "/api/logging",
        headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["level"] == "INFO"
    assert LoggingRepository().get_level() == str(INFO)

def test_set_logging_level_to_debug_200(
    client: FlaskClient, basic_admin_auth: Dict
) -> None:
    response = client.put(
        "/api/logging", json={"level": "DEBUG"},
        headers={**json_content_type_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["level"] == "DEBUG"
    assert LoggingRepository().get_level() == str(DEBUG)

def test_set_logging_level_to_notset_400(
    client: FlaskClient, basic_admin_auth: Dict
) -> None:
    response = client.put(
        "/api/logging", json={"level": "NOTSET"},
        headers={**json_content_type_header(), **basic_admin_auth}
    )
    assert response.status_code == 400
    assert response.json["description"] == "Must be one of: CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG."
