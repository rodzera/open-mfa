from os import kill
from signal import SIGTERM

from src.app.utils.helpers.logs import get_logger
from src.app.configs.constants import PRODUCTION_ENV, DIR_PATH

log = get_logger(__name__)


def terminate_server() -> None:
    """
    Terminates the current Flask server (Werkzeug WSGI or Gunicorn).
    :return: None
    """
    if PRODUCTION_ENV and (app_pid := get_gunicorn_pid()):
        kill(app_pid, SIGTERM)
    else:
        exit(1)


def get_gunicorn_pid() -> int:
    try:
        with open(DIR_PATH + "/gunicorn.pid") as f:
            return int(f.readline())
    except FileNotFoundError:
        log.error("Gunicorn pid not defined. Exiting")
    except ProcessLookupError:
        log.error("Gunicorn master process not found. Exiting")
    return 0
