from signal import SIGTERM
from os import kill, getenv

from src.app.configs.constants import DIR_PATH

__all__ = ["terminate_server"]


def terminate_server() -> None:
    """
    Terminates the current Flask server (Werkzeug WSGI or Gunicorn).
    :return: None
    """
    if getenv("_DEBUG"):
        exit(1)
    else:
        kill(get_gunicorn_pid(), SIGTERM)

def get_gunicorn_pid() -> int:
    with open(DIR_PATH + "/gunicorn.pid") as f:
        return int(f.readline())
