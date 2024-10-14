from pydantic import TypeAdapter
from sqlalchemy import select
from models.autor import AutorModel
from schemas.autor import  AutorSchema, AutoresSchemaRequest
from .base import Controller
from utils.exceptions import InvalidAutorException

class AutorController(Controller[AutorModel]):

    def get_all_autors(self) -> list[AutorSchema]:
        """
        Devuelve una lista de todos los autores en la base de datos
        
        Returns:
            list[AutorSchema]: lista de autores
        """
        query = select(AutorModel)
        autores = self.session.execute(query).scalars().all()
        autores_schema = [AutorSchema.from_orm(autor).model_dump() for autor in autores]
        return autores_schema

    def get_autor_by_id(self, id: int) -> AutorSchema:
        """
        Devuelve un autor por su id

        Args:
            id (int): El id del autor a obtener

        Returns:
            AutorSchema: El autor obtenido

        Raises:
            InvalidAutorException: Si el autor no existe
        """
        query = select(AutorModel).where(AutorModel.id == id)
        autor = self.session.execute(query).scalar()
        if autor:
            return AutorSchema.from_orm(autor).model_dump()
        else:
            raise InvalidAutorException("Autor no encontrado")
        
    def insert_autor(self, autor: AutoresSchemaRequest) -> AutorSchema:
        """
        Inserta un nuevo autor

        Args:
            author: El autor a insertar

        Returns:
            El autor insertado
        """
        new_author = AutorModel(
            nombre=autor.nombre,
            apellido=autor.apellido,
            fecha_nacimiento=autor.fecha_nacimiento
        )
        self.session.add(new_author)
        self.session.commit()
        return AutorSchema.from_orm(new_author).model_dump()
    
    def update_autor(self, id: int, autor: AutoresSchemaRequest) -> AutorSchema:
        """
        Actualiza un autor por su id

        Args:
            id (int): El id del autor a actualizar
            author (AutoresSchemaRequest): Los datos del autor a actualizar

        Returns:
            AutorSchema: El autor actualizado

        Raises:
            InvalidAutorException: Si el autor no existe
        """
        query = select(AutorModel).where(AutorModel.id == id)
        autor = self.session.execute(query).scalar()
        if not autor:
            raise InvalidAutorException("Autor no encontrado")
        
        autor.nombre = autor.nombre
        autor.apellido = autor.apellido
        autor.fecha_nacimiento = autor.fecha_nacimiento
        self.session.commit()
        return AutorSchema.from_orm(autor).model_dump()
    
    def delete_autor(self, id: int):
        """
        Elimina un autor por su id

        Args:
            id (int): El id del autor a eliminar

        Raises:
            InvalidAutorException: Si el autor no existe
        """
        query = select(AutorModel).where(AutorModel.id == id)
        autor = self.session.execute(query).scalar()
        if not autor:
            raise InvalidAutorException("Autor no encontrado")
        self.session.delete(autor)
        self.session.commit()
        return {"message": "Autor eliminado"}
