from time import time
from datetime import datetime
from flask.testing import FlaskClient
from pytest_mock import MockerFixture
from unittest.mock import MagicMock

from src.app.configs.constants import VERSION
from src.tests.utils import basic_admin_auth, json_accept_header


def test_database_200_up(
    client: FlaskClient, redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.resources.api.admin.status.redis_service"
    )
    mock_redis_service.current_timestamp = int(time())
    mock_redis_service.info.get.return_value = "redis_version"
    response = client.get(
        "/api/database", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["datetime"] == mock_redis_service.current_timestamp
    assert response.json["status"] == "up"
    assert response.json["version"] == mock_redis_service.info.get.return_value

def test_database_200_down(
    client: FlaskClient, redis_db: MagicMock, mocker: MockerFixture
) -> None:
    mock_redis_service = mocker.patch(
        "src.app.resources.api.admin.status.redis_service"
    )
    mock_redis_service.current_timestamp = False
    response = client.get(
        "/api/database", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["status"] == "down"

def test_server_200(client: FlaskClient, redis_db: MagicMock) -> None:
    response = client.get(
        "/api/server", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json["datetime"] == datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    assert response.json["status"] == "up"
    assert response.json["version"] == VERSION
