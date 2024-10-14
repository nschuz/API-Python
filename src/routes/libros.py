from flask import Blueprint, g, request, jsonify
from controllers.libro import LibroController
from utils.exceptions import InvalidAutorException, InvalidLibroException
from schemas.libro import LibrosSchemaRequest
libros_blueprint = Blueprint("libros", __name__, url_prefix="/libros")



@libros_blueprint.route("/", methods=["GET", "POST"])
def libros():
    
    """
    Obtiene o inserta un libro
    
    Returns:
        Un objeto con una lista de todos los libros si se utiliza el metodo GET
        Un objeto con los datos del libro insertado si se utiliza el metodo POST
    
    Raises:
        InvalidAutorException: Si el autor no existe
        Exception: En caso de error desconocido
    """
    try:
        
        session = g.session
        libro_controller = LibroController(session)
        
        if request.method == "GET":
            libros_list = libro_controller.get_all_books()
            return jsonify(libros_list), 200
        
        elif request.method == "POST":
            data = LibrosSchemaRequest(**request.json)
            nuevo_libro = libro_controller.insert_book(data)
            return jsonify(nuevo_libro), 201
    
    except InvalidAutorException as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@libros_blueprint.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def libro_detail(id):
    """
    Obtiene, actualiza o elimina un libro por su id
    
    Args:
        id (int): El id del libro a obtener, actualizar o eliminar
    
    Returns:
        Un objeto con los datos del libro si se utiliza el metodo GET
        Un objeto con los datos del libro actualizado si se utiliza el metodo PUT
        Un objeto con el mensaje "Libro eliminado" si se utiliza el metodo DELETE
    
    Raises:
        InvalidAutorException: Si el autor no existe
        InvalidLibroException: Si el libro no existe
    """
    try: 
        session = g.session
        libro_controller = LibroController(session)
        
        if request.method == "GET":
            libro = libro_controller.get_book_by_id(id)
            if libro:
                return jsonify(libro), 200
            else:
                return jsonify({"error": "Libro no encontrado"}), 404
        
        elif request.method == "PUT":
            data = LibrosSchemaRequest(**request.json)
            libro_actualizado = libro_controller.update_book(id, data)
            return jsonify(libro_actualizado), 200
        
        elif request.method == "DELETE":
            libro_controller.delete_book(id)
            return jsonify({"message": "Libro eliminado"}), 204
    
    #TODO GENERIC EXCEPTION HANDLER
    except InvalidAutorException as e:
        return jsonify({"error": str(e)}), 400
    
    except InvalidLibroException as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500