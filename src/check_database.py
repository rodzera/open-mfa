from os import environ
from pymysql import Error as MySQLError, connect as mysql_connect
from psycopg2 import Error as PgSQLError, connect as pgsql_connect

from logging import getLogger

log = getLogger(__name__)


def database_check():
    connectors = {
        "mysql": mysql_connect,
        "postgresql": pgsql_connect
    }

    try:
        provider = environ["_DB_PROVIDER"]
        connection = connectors[provider](
            ** {
                "host": environ["_DB_HOST"],
                "user": "admin",
                "password": environ["_DB_PASS"],
                "database": environ["_DB_DATABASE"]
            }
        )
        if connection:
            log.debug(f"{provider.upper()} database connected successfully")
            return 1

    except KeyError as e:
        log.error(f"Missing env variable: {e}")
        raise ValueError(f"Missing env variable: {e}")
    except MySQLError as e:
        log.error(f"Error connecting to mysql database: {e}")
    except PgSQLError as e:
        log.error(f"Error connecting to postgresql database: {e}")
    return 0
