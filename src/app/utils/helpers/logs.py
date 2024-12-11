from os import path, makedirs
from logging import getLogger, Logger

__all__ = ["get_logger"]


_log_dir = "./logs"
if not path.exists(_log_dir):
    makedirs(_log_dir)

def get_logger(name: str) -> Logger:
    return getLogger("open-mfa." + name) if not name.startswith("redis") else getLogger("redis")
