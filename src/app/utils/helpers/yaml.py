from yaml import SafeLoader, load

from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


def get_project_version(dir_path: str) -> str:
    try:
        with open(dir_path + "/version.yaml", "r") as file:
            data = load(file, Loader=SafeLoader)
            return data["version"]
    except Exception as e:
        from src.app.infra.signals import terminate_server
        log.error(f"Error loading version.yaml: {e}")
        terminate_server()
