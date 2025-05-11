from typing import Optional
from yaml import SafeLoader, load
from src.app.utils.helpers.logging import get_logger

log = get_logger(__name__)


def get_project_version(path: str) -> Optional[str]:
    try:
        with open(f"{path}/version.yaml", "r") as file:
            data = load(file, Loader=SafeLoader)
            return data["version"]
    except Exception as e:
        from src.infra.signals import terminate_server
        log.error(f"Error loading version.yaml: {e}")
        return terminate_server()
