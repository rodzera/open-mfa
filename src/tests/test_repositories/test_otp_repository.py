from unittest.mock import MagicMock

from src.app.repositories.oath import OTPRepository


def test_service_type_attr():
    assert OTPRepository._service_type == "otp"

def test_set_otp_as_used() -> None:
    mock_self = MagicMock()
    OTPRepository.set_otp_as_used(mock_self)
    mock_self.redis.db.assert_called_once_with(
        "hset", mock_self._oath_session_key, mapping={"used": 1}
    )
