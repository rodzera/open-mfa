from pytest_mock import MockerFixture
from unittest.mock import PropertyMock

from src.app.infra.redis import RedisService, redis_service


def test_db_method(mocker: MockerFixture) -> None:
    mock_client_prop = mocker.patch.object(
        RedisService, "client", new_callable=PropertyMock, create=True
    )

    db = redis_service.db("hset", "key", mapping={"another_key": "value"})

    assert db == mock_client_prop.return_value.hset.return_value
    mock_client_prop.return_value.hset.assert_called_once_with(
        "key", mapping={"another_key": "value"}
    )

def test_setup_connection_method(mocker: MockerFixture) -> None:
    mock_redis_cls = mocker.patch("src.app.infra.redis.StrictRedis")
    mock_environ = mocker.patch("src.app.infra.redis.environ")
    environ = {
        "_REDIS_HOST": "localhost",
        "_REDIS_PASS": "s3cr3t"
    }
    mock_environ.__getitem__.side_effect = environ.__getitem__

    redis_client = redis_service.setup_connection()

    assert redis_client == mock_redis_cls.return_value
    mock_redis_cls.assert_called_once_with(
        host="localhost",
        port="6379",
        password="s3cr3t",
        db=0,
        socket_timeout=5,
        decode_responses=True
    )

def test_info_prop(mocker: MockerFixture) -> None:
    mock_client_prop = mocker.patch.object(
        RedisService, "client", new_callable=PropertyMock, create=True
    )
    assert redis_service.info == mock_client_prop.return_value.info.return_value
