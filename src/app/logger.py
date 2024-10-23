import logging
from os import path, mkdir, getenv


def set_logger_level(level: str):
    logger_level = logging._nameToLevel.get(level)
    for name in logging.root.manager.loggerDict:
        if name.startswith("src."):
            logger = logging.getLogger(name)
            logger.setLevel(logger_level)
            for h in logger.handlers:
                h.setLevel(logger_level)


def get_logger(name: str = None) -> logging.Logger:
    default_level = logging.INFO
    handlers = []
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(funcName)s | %(lineno)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    sh = logging.StreamHandler()
    sh.setLevel(default_level)
    sh.setFormatter(formatter)
    handlers.append(sh)

    if not getenv("_TESTING"):
        if not path.exists("logs"):
            mkdir("logs")

        fh = logging.FileHandler("logs/app.log", mode="a")
        fh.setLevel(default_level)
        fh.setFormatter(formatter)
        handlers.append(fh)

    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers
    )

    logger = logging.getLogger(name)
    logger.setLevel(default_level)
    return logger
