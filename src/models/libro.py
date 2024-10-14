from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from .base import BaseModel
#Base = declarative_base()


class LibroModel(BaseModel):
    __tablename__ = 'libro'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    autor_id = Column(Integer, ForeignKey('autor.id', ondelete='RESTRICT'), nullable=False)
    
    autor = relationship('AutorModel', back_populates='libros')
