import importlib
import inspect
import os
import pkgutil

from flask import Flask, Blueprint
from flask.logging import default_handler

from music_management.config import ENVIRONMENTS, ConfigEnum
from music_management.extensions import db_context, alembic
from music_management.middleware import add_content_type_header
from music_management.resources.ping import ping_blueprint


def __get_blueprint_from_resource_module():
    modules = importlib.import_module("music_management.resources")

    packages = [item for item in pkgutil.walk_packages(modules.__path__) if item.ispkg is True]

    blueprints = list()

    for _loader, name, is_pkg in packages:
        resource_route_module = importlib.import_module(f"music_management.resources.{name}.routes")
        members = inspect.getmembers(resource_route_module)

        module_blueprints = [item[1] for item in members if isinstance(item[1], Blueprint)]

        blueprints += module_blueprints

    return blueprints


def register_blueprints(app):
    blueprints = __get_blueprint_from_resource_module()

    for bp in blueprints:
        app.register_blueprint(bp)

    app.register_blueprint(ping_blueprint)


def register_extensions(app):
    db_context.init_app(app)
    alembic.init_app(app, True, "db")
    return None


def register_middlewares(app):
    app.after_request(add_content_type_header)
    return None


def register_logging(app):
    app.logger.addHandler(default_handler)
    return None


def create_app(env=None):
    app = Flask(__name__)
    config_env = env if env is not None else ConfigEnum(os.getenv("FLASK_ENV", "development"))
    app.config.from_object(ENVIRONMENTS[config_env])
    register_extensions(app)
    register_blueprints(app)
    register_middlewares(app)
    register_logging(app)

    with app.app_context():
        alembic.upgrade()

    return app


if __name__ == '__main__':
    create_app().run()
