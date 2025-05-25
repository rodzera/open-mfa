from os import getenv
from pathlib import Path

current_path = Path(__file__).parent.resolve()

host = getenv("HOST", "0.0.0.0")
port = getenv("PORT", "8080")
bind = f"{host}:{port}"
backlog = 2048

worker_class = "gthread"
workers = getenv("WORKERS", 2)
threads = getenv("THREADS", 4)
timeout = 30
graceful_timeout = 30

proc_name = "open-mfa"
pidfile = f"{current_path}/gunicorn.pid"
logconfig = f"{current_path}/log.conf"

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

max_requests = 1000
max_requests_jitter = 200