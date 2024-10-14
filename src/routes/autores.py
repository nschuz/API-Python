from flask import Blueprint, g, request, jsonify
from controllers.autores import AutorController
from controllers.libro import LibroController
from utils.exceptions import InvalidAutorException
from schemas.autor import AutoresSchemaRequest

autores_blueprint = Blueprint("autores", __name__, url_prefix="/autores")

@autores_blueprint.route("/", methods=["GET", "POST"])
def autores():
    """
    Obtiene o inserta un autor
    
    Returns:
        Un objeto con una lista de todos los autores si se utiliza el método GET
        Un objeto con los datos del autor insertado si se utiliza el método POST
    
    Raises:
        Exception: En caso de error desconocido
    """
    try:
        session = g.session
        autor_controller = AutorController(session)
        if request.method == "GET":
            autores_list = autor_controller.get_all_autors()
            return jsonify(autores_list), 200
        
        elif request.method == "POST":
            data = AutoresSchemaRequest(**request.json)
            nuevo_autor = autor_controller.insert_autor(data)
            return jsonify(nuevo_autor), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@autores_blueprint.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def autor_detail(id):
    """
    Obtiene, actualiza o elimina un autor por su id
    
    Args:
        id (int): El id del autor a obtener, actualizar o eliminar
    
    Returns:
        Un objeto con los datos del autor si se utiliza el método GET
        Un objeto con los datos del autor actualizado si se utiliza el método PUT
        Un objeto con el mensaje "Autor eliminado" si se utiliza el método DELETE
    
    Raises:
        InvalidAuthorException: Si el autor no existe
        Exception: En caso de error desconocido
    """
    try:
        session = g.session
        autor_controller = AutorController(session)
        libro_controller = LibroController(session)  #
        
        if request.method == "GET":
            autor = autor_controller.get_autor_by_id(id)
            if autor:
                return jsonify(autor), 200
            else:
                return jsonify({"error": "Autor no encontrado"}), 404
        
        elif request.method == "PUT":
            data = AutoresSchemaRequest(**request.json)
            autor_actualizado = autor_controller.update_autor(id, data)
            return jsonify(autor_actualizado), 200
        
        elif request.method == "DELETE":

            libros_asociados = libro_controller.get_books_by_autor(id)
            if libros_asociados:
                return jsonify({"error": "No se puede eliminar el autor, tiene libros asociados"}), 400
            
            autor_controller.delete_autor(id)
            return jsonify({"message": "Autor eliminado"}), 200
    
    except InvalidAutorException as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

