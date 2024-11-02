from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from src.app.resources.api.index import *
from src.app.resources.api.status import *
from src.app.resources.api.otp import *
from src.app.resources.api.hotp import *
from src.app.resources.api.totp import *
