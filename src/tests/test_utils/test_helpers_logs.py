from src.app.utils.helpers.logs import mask_secrets_items


def test_mask_secrets_items():
    mock_data = {
        "otp": "666666",
        "secret": "s3cr3t",
        "uri": "otpauth://totp/open-mfa:testing_id?secret=s3cr3t&issuer=open-mfa&algorithm=SHA256",
        "last_used_otp": "666666",
        "key": 0,
        "count": 0
    }

    mock_nested_data = {**mock_data, "nested_data": {**mock_data}}
    data = mask_secrets_items(mock_nested_data)

    assert data["otp"] == "******"
    assert data["secret"] == "******"
    assert data["uri"] == "otpauth://totp/open-mfa:testing_id?secret=******&issuer=open-mfa&algorithm=SHA256"
    assert data["last_used_otp"] == "******"
    assert data["key"] == 0
    assert data["count"] == "******"
    assert data["nested_data"]["otp"] == "******"
    assert data["nested_data"]["secret"] == "******"
    assert data["nested_data"]["uri"] == "otpauth://totp/open-mfa:testing_id?secret=******&issuer=open-mfa&algorithm=SHA256"
    assert data["nested_data"]["last_used_otp"] == "******"
    assert data["nested_data"]["key"] == 0
    assert data["nested_data"]["count"] == "******"
