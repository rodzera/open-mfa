from os import path, getenv
from pathlib import Path

VERSION = "1.0.0"
DIR_PATH = str(Path(path.dirname(path.realpath(__file__))).parent)
TESTING_ENV = getenv("_TESTING")
DEVELOPMENT_ENV = getenv("_DEBUG")
PRODUCTION_ENV = (not DEVELOPMENT_ENV and not TESTING_ENV)
