from unittest.mock import MagicMock

from src.app.repositories.oath import TOTPRepository


def test_service_type_attr():
    assert TOTPRepository._service_type == "totp"

def test_set_last_used_otp() -> None:
    mock_self = MagicMock()
    client_otp = "123456"
    TOTPRepository.set_last_used_otp(mock_self, client_otp)
    mock_self.redis.db.assert_called_once_with(
        "hset", mock_self._oath_session_key,
        mapping={"last_used_otp": client_otp}
    )
