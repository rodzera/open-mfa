from re import search
from pyotp import TOTP

from flask.testing import FlaskClient


def test_totp_create_and_verify_request_200_success(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/totp", query_string={"interval": 30})
    assert create_response.status_code == 200

    totp_uri = create_response.json["uri"]
    secret_match = search(r"secret=([A-Z2-7]+)", totp_uri)
    secret = secret_match.group(1)
    totp = TOTP(secret)
    current_otp = totp.now()

    verify_response = client.get(f"/api/totp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

def test_totp_create_and_verify_wrong_otp_200_failure(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/totp")
    assert create_response.status_code == 200

    wrong_otp = "000000"
    verify_response = client.get(f"/api/totp?otp={wrong_otp}")

    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_totp_create_and_verify_already_used_otp_200_failure(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/totp", query_string={"interval": 30})
    assert create_response.status_code == 200

    totp_uri = create_response.json["uri"]
    secret_match = search(r"secret=([A-Z2-7]+)", totp_uri)
    secret = secret_match.group(1)
    totp = TOTP(secret)
    current_otp = totp.now()

    verify_response = client.get(f"/api/totp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

    verify_response = client.get(f"/api/totp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_totp_create_already_created_409(client: FlaskClient) -> None:
    create_response = client.get("/api/totp", query_string={"interval": 30})
    assert create_response.status_code == 200

    create_response = client.get("/api/totp", query_string={"interval": 30})
    assert create_response.status_code == 409
    assert create_response.json["description"] == "TOTP already created"

def test_totp_create_totp_interval_invalid_range_400(
    client: FlaskClient
) -> None:
    response = client.get("/api/totp", query_string={"interval": 10})
    assert response.status_code == 400
    assert response.json["description"] == (
        "Must be greater than or equal to 30 and less than or equal to 60."
    )

def test_totp_verify_totp_not_created_404(client: FlaskClient) -> None:
    response = client.get("/api/totp", query_string={"otp": "123456"})
    assert response.status_code == 404
    assert response.json["description"] == "TOTP not created"

def test_totp_verify_totp_is_not_digit_400(client: FlaskClient) -> None:
    response = client.get("/api/totp", query_string={"otp": "ABCDEF"})
    assert response.status_code == 400
    assert response.json["description"] == "OTP must be a 6-digit string"

def test_totp_verify_totp_different_len_400(client: FlaskClient) -> None:
    response = client.get("/api/totp", query_string={"otp": "123"})
    assert response.status_code == 400
    assert response.json["description"] == "OTP must be a 6-digit string"
