from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import BaseModel
#Base = declarative_base()

class AutorModel(BaseModel):
    __tablename__ = 'autor'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)

    # Utilizamos el nombre del modelo como string
    libros = relationship('LibroModel', back_populates='autor', cascade='all, delete-orphan')
