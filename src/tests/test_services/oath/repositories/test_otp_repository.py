from unittest.mock import MagicMock

from src.app.services.oath.repositories import OTPRepository


def test_service_type_attr():
    assert OTPRepository._service_type == "otp"

def test_set_otp_as_used(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    OTPRepository.set_otp_as_used(mock_self)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key, mapping={"used": 1}
    )
