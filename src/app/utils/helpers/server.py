from src.app.configs.constants import DIR_PATH
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


def get_gunicorn_pid() -> int:
    try:
        with open(DIR_PATH + "/gunicorn.pid") as f:
            return int(f.readline())
    except FileNotFoundError:
        log.error("Gunicorn pid not defined. Exiting")
    except ProcessLookupError:
        log.error("Gunicorn master process not found. Exiting")
    return 0
