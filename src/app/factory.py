from flask import Flask
from flasgger import Swagger

from src.app.schemas import ma
from src.app.logger import get_logger
from src.app.configs.environ import DefaultConfig
from src.app.utils import log_json_after_request
from src.app.utils.handlers.request import set_session_id_before_request

log = get_logger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_prefixed_env(prefix="")  # variables starting with an underscore will be loaded
    app.config.from_object(DefaultConfig.set_flask_config(**app.config))

    log.info("Initializing marshmallow")
    ma.init_app(app)

    log.info("Initializing swagger")
    Swagger(app, template_file="swagger.yaml")

    from src.app.resources.api import api
    from src.app.resources.views import views
    log.info("Registering blueprints")
    app.register_blueprint(api)
    app.register_blueprint(views)

    log.info("Registering after and before request funcs")
    app.before_request(set_session_id_before_request)
    app.after_request(log_json_after_request)

    from src.app.utils.handlers.errors import register_error_handlers
    log.info("Registering error handlers")
    register_error_handlers(app)

    log.info("Server is ready")
    return app