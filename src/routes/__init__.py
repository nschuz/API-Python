from flask import Flask

from .health_check import health_check_blueprint
from .libros import libros_blueprint
from .autores import autores_blueprint


def register(app: Flask) -> None:
    app.register_blueprint(health_check_blueprint)
    app.register_blueprint(libros_blueprint)
    app.register_blueprint(autores_blueprint)