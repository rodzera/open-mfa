from yaml import SafeLoader, load

from src.app.utils.helpers.logs import get_logger

log = get_logger(__name__)

__all__ = ["get_project_version"]


def get_project_version(dir_path: str) -> str:
    try:
        with open(dir_path + "/version.yaml", "r") as file:
            data = load(file, Loader=SafeLoader)
            return data["version"]
    except Exception as e:
        log.error(f"Error loading version.yaml: {e}")
        exit(1)
