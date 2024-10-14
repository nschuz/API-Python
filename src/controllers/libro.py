from pydantic import TypeAdapter
from sqlalchemy import select
from models.libro import LibroModel
from schemas.libro import LibroSchema, LibrosSchemaRequest
from .base import Controller
from utils.exceptions import InvalidAutorException, InvalidLibroException

class LibroController(Controller[LibroModel]):


    def get_all_books(self) -> list[LibroSchema]:
        """
        Devuelve una lista de todos los libros en la base de datos
        
        Returns:
            list[LibroSchema]: lista de libros
        """
        query = select(LibroModel)
        libros = self.session.execute(query).scalars().all()
        libros_schema = [LibroSchema.from_orm(libro).model_dump() for libro in libros]
        return libros_schema

    def get_book_by_id(self, id: int) -> LibroSchema:
        """
        Devuelve un libro por su id

        Args:
            id (int): El id del libro a obtener

        Returns:
            LibroSchema: El libro obtenido

        Raises:
            InvalidLibroException: Si el libro no existe
        """
        query = select(LibroModel).where(LibroModel.id == id)
        libro = self.session.execute(query).scalar()
        if libro:
            return LibroSchema.from_orm(libro).model_dump()
        else:
            return None
        
    def insert_book(self, book: LibrosSchemaRequest) -> LibroSchema:
        
        """
        Inserta un nuevo libro

        Args:
            book: El libro a insertar

        Returns:
            El libro insertado

        Raises:
            InvalidAutorException: Si el autor no existe
        """
        query = select(LibroModel).where(LibroModel.autor_id == book.autor_id)
        autor = self.session.execute(query).scalar()
        if not autor:
            raise InvalidAutorException("Autor no encontrado")
        
        new_book = LibroModel(
            titulo=book.titulo,
            fecha_publicacion=book.fecha_publicacion,
            autor_id=book.autor_id
        )
        self.session.add(new_book)
        self.session.commit()
        return LibroSchema.from_orm(new_book).model_dump()
    

    def update_book(self, id: int, book: LibrosSchemaRequest) -> LibroSchema:
        """
        Actualiza un libro por su id

        Args:
            id (int): El id del libro a actualizar
            book (LibrosSchemaRequest): Los datos del libro a actualizar

        Returns:
            LibroSchema: El libro actualizado

        Raises:
            InvalidAutorException: Si el autor no existe
            InvalidLibroException: Si el libro no existe
        """
        query = select(LibroModel).where(LibroModel.id == id)
        libro = self.session.execute(query).scalar()
        if not libro:
            raise InvalidAutorException("Libro no encontrado")
        
        query = select(LibroModel).where(LibroModel.autor_id == book.autor_id)
        autor = self.session.execute(query).scalar()
        if not autor:
            raise InvalidAutorException("Autor no encontrado")
        
        libro.titulo = book.titulo
        libro.fecha_publicacion = book.fecha_publicacion
        libro.autor_id = book.autor_id
        self.session.commit()
        return LibroSchema.from_orm(libro).model_dump() 
    
    
    def delete_book(self, id: int):
        """
        Elimina un libro por su id

        Args:
            id (int): El id del libro a eliminar

        Raises:
            InvalidLibroException: Si el libro no existe
        """
        query = select(LibroModel).where(LibroModel.id == id)
        libro = self.session.execute(query).scalar()
        if not libro:
            raise InvalidLibroException("Libro no encontrado")
        self.session.delete(libro)
        self.session.commit()
        return {"message": "Libro eliminado"}
    
    
    def get_books_by_autor(self, author_id: int) -> list[LibroSchema]:
        """
        Obtiene todos los libros de un autor

        Args:
            author_id (int): El id del autor

        Returns:
            list[LibroSchema]: La lista de libros del autor
        """
        query = select(LibroModel).where(LibroModel.autor_id == author_id)
        libros = self.session.execute(query).scalars().all()
        libros_schema = [LibroSchema.from_orm(libro).model_dump() for libro in libros]
        return libros_schema