from flask import Blueprint

views = Blueprint("views", __name__)

from src.app.resources.views.index import *
