from typing import Dict
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from src.tests.utils import json_accept_header


def test_database_200(
    client: FlaskClient, mocker: MockerFixture, basic_admin_auth: Dict
) -> None:
    mock_controller = mocker.patch(
        "src.app.resources.api.admin.healthcheck.HealthCheckController"
    )
    mock_controller.return_value.get_db_status.return_value = {"test": "test"}
    response = client.get(
        "/api/database", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json == mock_controller.return_value.get_db_status.return_value


def test_server_200(
    client: FlaskClient, mocker: MockerFixture, basic_admin_auth: Dict
) -> None:
    mock_controller = mocker.patch(
        "src.app.resources.api.admin.healthcheck.HealthCheckController"
    )
    mock_controller.return_value.get_server_status.return_value = {"test": "test"}
    response = client.get(
        "/api/server", headers={**json_accept_header(), **basic_admin_auth}
    )
    assert response.status_code == 200
    assert response.json == mock_controller.return_value.get_server_status.return_value
