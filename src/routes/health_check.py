from flask import Blueprint, g
from controllers.libro import LibroController

health_check_blueprint = Blueprint("health_check", __name__, url_prefix="/health-check")


@health_check_blueprint.route("/")
def health_check():
    """
    Endpoint para verificar el estado de la aplicaci n.

    Requiere una sesi n abierta.

    Returns:
        str: "OK"
    """
    session = g.session
    users_list = LibroController(session).list_all()
    print(users_list)
    return "OK"