import logging
from os import kill
from sys import exit as sys_exit
from signal import signal, SIGUSR1, SIGTERM

from src.app.utils.helpers.logging import get_logger
from src.app.configs.constants import PRODUCTION_ENV
from src.app.utils.helpers.server import get_gunicorn_pid

log = get_logger(__name__)


def terminate_server() -> None:
    """
    Terminates the current web server (Werkzeug WSGI or Gunicorn).
    :return: None
    """
    if PRODUCTION_ENV and (app_pid := get_gunicorn_pid()):
        kill(app_pid, SIGTERM)
    else:
        sys_exit(1)


def send_logging_signal() -> None:
    """
    This function sends signal to the gunicorn master process,
    triggering all workers to change its logging level.
    :return:
    """
    app_pid = get_gunicorn_pid()
    log.debug(f"Sending a SIGUSR1 signal to the gunicorn master process")

    try:
        kill(app_pid, SIGUSR1)
    except Exception:
        log.exception("Exception occurred while sending a SIGUSR1 signal")


def register_gunicorn_signal_handler(*args) -> None:
    """
    This function register a signal handler function that is going to be
    caught by the gunicorn master process when a SIGUSR1 signal is thrown.
    It will only be registered in a production environment.
    :return:
    """
    if PRODUCTION_ENV:
        signal(SIGUSR1, logging_signal_handler)


def logging_signal_handler(*args) -> None:
    """
    This function will be used by each gunicorn worker to change its
    logging level.

    :param *args: SIGUSR1, frame
    :return:
    """
    from src.app.infra.logging import logging_infra
    from src.app.repositories.logging import LoggingRepository

    level = int(
        LoggingRepository().get_level() or
        logging_infra.DEFAULT_LEVEL
    )

    if level != logging.root.level:
        logging_infra.set_level(level)
