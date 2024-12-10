from logging import getLogger, Logger

__all__ = ["get_logger"]


def get_logger(name: str) -> Logger:
    return getLogger("open-mfa." + name) if not name.startswith("redis") else getLogger("redis")
