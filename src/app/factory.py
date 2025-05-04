from flask import Flask
from flasgger import Swagger

from src.app.schemas import ma
from src.app.infra.logging import logging_service
from src.app.configs.environ import DefaultConfig
from src.app.utils.helpers.logging import get_logger
from src.app.infra.middlewares.errors import register_error_handlers
from src.app.infra.signals import register_gunicorn_signal_handler
from src.app.infra.middlewares.user_session import trigger_user_session_service

log = get_logger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    logging_service.configure_loggers()

    log.info("Setting app configuration")
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

    log.info("Registering request funcs")
    app.before_request(trigger_user_session_service)

    log.info("Registering error handlers")
    register_error_handlers(app)

    register_gunicorn_signal_handler()
    log.info("Server is ready")

    return app
