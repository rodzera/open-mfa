from unittest.mock import MagicMock

from src.app.services.oath.repositories import HOTPRepository


def test_service_type_attr():
    assert HOTPRepository._service_type == "hotp"

def test_increase_hotp_counter(redis_db: MagicMock) -> None:
    mock_self = MagicMock()
    counter = 0
    HOTPRepository.increase_hotp_counter(mock_self, counter)
    redis_db.assert_called_once_with(
        "hset", mock_self._session_key,
        mapping={"count": counter + 1}
    )
