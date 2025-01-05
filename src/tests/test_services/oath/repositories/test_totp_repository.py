from unittest.mock import MagicMock

from src.app.services.oath.repositories import TOTPRepository


def test_service_type_attr():
    assert TOTPRepository._service_type == "totp"

def test_set_last_used_otp(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    client_otp = "123456"
    TOTPRepository.set_last_used_otp(mock_self, client_otp)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"last_used_otp": client_otp}
    )
