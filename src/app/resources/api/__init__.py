from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from src.app.resources.api.index import *
from src.app.resources.api.status import *