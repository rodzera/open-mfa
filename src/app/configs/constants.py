from pathlib import Path
from os import path, getenv

from src.app.utils.helpers.yaml import get_project_version


DIR_PATH = str(Path(path.dirname(path.realpath(__file__))).parent)
VERSION = get_project_version(DIR_PATH)
TESTING_ENV = getenv("_TESTING")
DEVELOPMENT_ENV = getenv("_DEBUG")
PRODUCTION_ENV = (not DEVELOPMENT_ENV and not TESTING_ENV)
