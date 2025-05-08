from werkzeug.exceptions import HTTPException


class RedisUnavailableError(HTTPException):
    code: int = 503
    description: str = "Redis is unavailable or failed to connect."
