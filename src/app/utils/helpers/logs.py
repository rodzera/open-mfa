from re import sub
from typing import Dict, Union
from logging import getLogger, Logger


def get_logger(name: str) -> Logger:
    return getLogger("open-mfa." + name) if not name.startswith("redis") else getLogger("redis")


def mask_secrets_items(data: Dict[str, Union[Dict, str]]) -> Dict[str, Union[Dict, str]]:
    masked_data = {}

    for key, value in data.items():
        if any([otp in key for otp in ("secret", "otp", "count")]):
            masked_data[key] = "******"
        elif isinstance(value, str) and "secret=" in value:
            masked_data[key] = sub(r"secret=[^&]+", "secret=******", value)
        elif isinstance(value, dict):
            masked_data[key] = mask_secrets_items(value)
        else:
            masked_data[key] = value

    return masked_data
