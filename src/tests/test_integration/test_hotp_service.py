from re import search
from pyotp import HOTP
from flask.testing import FlaskClient

from src.app.services.oath.hotp import HOTPService


def test_hotp_create_and_verify_request_200_twice_success(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/hotp")
    assert create_response.status_code == 200

    hotp_uri = create_response.json["uri"]
    secret_match = search(r"secret=([A-Z2-7]+)", hotp_uri)
    secret = secret_match.group(1)
    hotp = HOTP(secret, digest=HOTPService._hash_method)
    current_otp = hotp.at(0)

    verify_response = client.get(f"/api/hotp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

    current_otp = hotp.at(1)
    verify_response = client.get(f"/api/hotp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

def test_hotp_create_and_verify_request_200_twice_success_with_resync_protocol(
    client: FlaskClient
) -> None:
    create_response = client.get(
        "/api/hotp", query_string={"initial_count": 30}
    )
    assert create_response.status_code == 200

    hotp_uri = create_response.json["uri"]
    secret_match = search(r"secret=([A-Z2-7]+)", hotp_uri)
    secret = secret_match.group(1)
    client_hotp = HOTP(secret, digest=HOTPService._hash_method)
    desynchronized_otp = client_hotp.at(35)

    verify_response = client.get(
        "/api/hotp", query_string={"otp": desynchronized_otp}
    )
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

    synchronized_otp = client_hotp.at(36)
    verify_response = client.get(
        "/api/hotp", query_string={"otp": synchronized_otp}
    )
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

def test_hotp_create_and_verify_wrong_otp_200_failure(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/hotp")
    assert create_response.status_code == 200

    wrong_otp = "000000"
    verify_response = client.get(f"/api/hotp?otp={wrong_otp}")

    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_hotp_create_and_verify_wrong_otp_200_failure_with_resync_protocol(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/hotp")
    assert create_response.status_code == 200

    hotp_uri = create_response.json["uri"]
    secret_match = search(r"secret=([A-Z2-7]+)", hotp_uri)
    secret = secret_match.group(1)
    client_hotp = HOTP(secret, digest=HOTPService._hash_method)
    otp_out_of_the_resync_range = client_hotp.at(6)

    verify_response = client.get(
        "/api/hotp",
        query_string={"otp": otp_out_of_the_resync_range}
    )
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_hotp_create_and_verify_already_used_otp_200_failure(
    client: FlaskClient
) -> None:
    create_response = client.get(
        "/api/hotp", query_string={"initial_count": 30}
    )
    assert create_response.status_code == 200

    hotp_uri = create_response.json["uri"]
    secret_match = search(r"secret=([A-Z2-7]+)", hotp_uri)
    secret = secret_match.group(1)
    hotp = HOTP(secret, digest=HOTPService._hash_method)
    current_otp = hotp.at(30)

    verify_response = client.get(f"/api/hotp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

    verify_response = client.get(f"/api/hotp?otp={current_otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_hotp_create_already_created_409(client: FlaskClient) -> None:
    create_response = client.get(
        "/api/hotp", query_string={"initial_count": 30}
    )
    assert create_response.status_code == 200

    create_response = client.get(
        "/api/hotp", query_string={"initial_count": 30}
    )
    assert create_response.status_code == 409
    assert create_response.json["description"] == "HOTP already created"

def test_hotp_create_hotp_initial_count_invalid_range_400(
    client: FlaskClient
) -> None:
    response = client.get("/api/hotp", query_string={"initial_count": -1})
    assert response.status_code == 400
    assert response.json["description"] == (
        "Must be greater than or equal to 0."
    )

def test_hotp_create_hotp_resync_threshold_invalid_range_400(
    client: FlaskClient
) -> None:
    response = client.get("/api/hotp", query_string={"resync_threshold": 4})
    assert response.status_code == 400
    assert response.json["description"] == (
        "Must be greater than or equal to 5 and less than or equal to 10."
    )

def test_hotp_verify_hotp_not_created_404(client: FlaskClient) -> None:
    response = client.get("/api/hotp", query_string={"otp": "123456"})
    assert response.status_code == 404
    assert response.json["description"] == "HOTP not created"

def test_hotp_verify_hotp_is_not_digit_400(client: FlaskClient) -> None:
    response = client.get("/api/hotp", query_string={"otp": "ABCDEF"})
    assert response.status_code == 400
    assert response.json["description"] == "OTP must be a 6-digit string"

def test_hotp_verify_hotp_different_len_400(client: FlaskClient) -> None:
    response = client.get("/api/hotp", query_string={"otp": "123"})
    assert response.status_code == 400
    assert response.json["description"] == "OTP must be a 6-digit string"
