from typing import Dict
from datetime import datetime
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from src.app.configs.constants import APP_VERSION
from src.app.infra.redis import redis_service
from src.tests.utils import json_accept_header


def test_database_200_up(
    client: FlaskClient, basic_admin_auth: Dict
) -> None:
    response = client.get(
        "/api/database", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["datetime"] == redis_service.current_timestamp
    assert response.json["status"] == "up"
    assert response.json["version"] == "unknown"

def test_database_200_down(
    client: FlaskClient, mocker: MockerFixture, basic_admin_auth: Dict
) -> None:
    mock_redis_client_time = mocker.patch.object(
        redis_service.client, "time", side_effect=Exception()
    )
    response = client.get(
        "/api/database", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["status"] == "down"
    mock_redis_client_time.assert_called_once_with()

def test_server_200(
    client: FlaskClient, basic_admin_auth: Dict
) -> None:
    response = client.get(
        "/api/server", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["datetime"] == datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    assert response.json["status"] == "up"
    assert response.json["version"] == APP_VERSION
