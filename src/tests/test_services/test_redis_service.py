from datetime import timedelta
from flask.ctx import RequestContext
from pytest_mock import MockerFixture
from unittest.mock import PropertyMock

from src.app.services.redis import RedisService, redis_service


def test_client_is_none_for_testing_env() -> None:
    assert redis_service.client is None

def test_db_method(mocker: MockerFixture) -> None:
    mock_client_prop = mocker.patch.object(
        RedisService, "client", new_callable=PropertyMock, create=True
    )

    db = redis_service.db("hset", "key", mapping={"another_key": "value"})

    assert db == mock_client_prop.return_value.hset.return_value
    mock_client_prop.return_value.hset.assert_called_once_with(
        "key", mapping={"another_key": "value"}
    )

def test_insert_hset_method(mocker: MockerFixture) -> None:
    mock_db_method = mocker.patch.object(
        RedisService, "db", new_callable=PropertyMock
    )

    redis_service.insert_hset("key", {"another_key": "value"})

    mock_db_method.return_value.assert_has_calls([
        mocker.call("hset", "key", mapping={"another_key": "value"}),
        mocker.call("expire", "key", timedelta(minutes=60)),
    ])

def test_setup_connection_method(mocker: MockerFixture) -> None:
    mock_redis_cls = mocker.patch("src.app.services.redis.StrictRedis")
    mock_environ = mocker.patch("src.app.services.redis.environ")
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

def test_get_session_key_method(
    req_ctx: RequestContext, mocker: MockerFixture
) -> None:
    mock_session = mocker.patch("src.app.services.redis.session")
    sess = {"session_id": "123456"}
    mock_session.__getitem__.side_effect = sess.__getitem__

    session_key = redis_service.get_session_key("otp")
    assert session_key == f"{sess['session_id']}:otp"
