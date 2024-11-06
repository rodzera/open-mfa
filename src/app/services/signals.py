import logging
from os import kill
from logging import getLogger
from signal import signal, SIGUSR1

from src.app.services.redis import redis_service
from src.app.configs.constants import PRODUCTION_ENV, DIR_PATH

log = getLogger(__name__)


def send_logging_signal() -> None:
    """
    This function sends signal to the gunicorn master process,
    triggering all workers to change its logging level.
    :return:
    """
    if not PRODUCTION_ENV:
        return

    try:
        with open(DIR_PATH + "/gunicorn.pid") as f:
            app_pid = int(f.readline())

        log.debug(f"Sending a SIGUSR1 signal to the gunicorn master process")
        kill(app_pid, SIGUSR1)
    except FileNotFoundError:
        log.error("Gunicorn pid not defined. Exiting")
    except ProcessLookupError:
        log.error("Gunicorn master process not found. Exiting")
    except Exception:
        log.exception("Exception occurred while sending a SIGUSR1 signal")


def register_gunicorn_signal_handler() -> None:
    """
    This function register a signal handler function that is going to be
    caught by the gunicorn master process when a SIGUSR1 signal is thrown.
    It will only be registered in a production environment.
    :return:
    """
    if PRODUCTION_ENV:
        signal(SIGUSR1, gunicorn_signal_handler)


def gunicorn_signal_handler(*args) -> None:
    """
    This function will be used by each gunicorn worker to change its
    logging level.

    :param *args: SIGUSR1, frame
    :return:
    """
    from src.app.services.logs import logging_service

    level = int(
        redis_service.db("get", "log") or
        logging_service.DEFAULT_LEVEL
    )

    if level != logging.root.level:
        logging_service.set_logger_level(level)
