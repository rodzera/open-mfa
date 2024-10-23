from typing import Tuple, Union
from sqlalchemy import text, exc

from src.app.factory import db, get_logger

log = get_logger(__name__)

__all__ = ["get_db_timestamp"]


def get_db_timestamp() -> Union[str, bool]:
    log.info("Querying db current timestamp")
    try:
        with db.engine.connect() as conn:
            query = conn.execute(text("SELECT CURRENT_TIMESTAMP"))
            result = [row[0] for row in query]
            log.debug(f"Query result: {result}")
        return result[0].strftime("%Y-%m-%d %H:%M:%S")
    except exc.OperationalError as e:
        log.error(f"Error fetching db current timestamp: {e}")
        return False
