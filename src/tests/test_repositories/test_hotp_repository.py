from unittest.mock import MagicMock

from src.app.repositories.oath import HOTPRepository


def test_service_type_attr():
    assert HOTPRepository._service_type == "hotp"

def test_increase_hotp_counter() -> None:
    mock_self = MagicMock()
    counter = 0
    HOTPRepository.increase_hotp_counter(mock_self, counter)
    mock_self.redis.db.assert_called_once_with(
        "hset", mock_self._oath_session_key,
        mapping={"count": counter + 1}
    )
