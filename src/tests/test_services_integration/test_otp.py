from flask.testing import FlaskClient


def test_otp_create_and_verify_request_200_success(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/otp")
    assert create_response.status_code == 200

    otp = create_response.json["otp"]
    verify_response = client.get(f"/api/otp?otp={otp}")

    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

def test_otp_create_and_verify_wrong_otp_200_failure(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/otp")
    assert create_response.status_code == 200

    wrong_otp = "000000"
    verify_response = client.get(f"/api/otp?otp={wrong_otp}")

    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_otp_create_and_verify_already_used_otp_200_failure(
    client: FlaskClient
) -> None:
    create_response = client.get("/api/otp")
    assert create_response.status_code == 200
    otp = create_response.json["otp"]

    verify_response = client.get(f"/api/otp?otp={otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is True

    verify_response = client.get(f"/api/otp?otp={otp}")
    assert verify_response.status_code == 200
    assert verify_response.json["status"] is False

def test_otp_verify_otp_not_created_404(client: FlaskClient) -> None:
    response = client.get("/api/otp", query_string={"otp": "123456"})
    assert response.status_code == 404
    assert response.json["description"] == "OTP not created"

def test_otp_verify_otp_is_not_digit_400(client: FlaskClient) -> None:
    response = client.get("/api/otp", query_string={"otp": "ABCDEF"})
    assert response.status_code == 400
    assert response.json["description"] == "OTP must be a 6-digit string"

def test_otp_verify_otp_different_len_400(client: FlaskClient) -> None:
    response = client.get("/api/otp", query_string={"otp": "123"})
    assert response.status_code == 400
    assert response.json["description"] == "OTP must be a 6-digit string"
