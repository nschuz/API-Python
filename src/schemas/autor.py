from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class AutorSchema(BaseModel):
    id: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    
    class Config:
        from_attributes=True
        orm_mode=True

class AutoresSchemaRequest(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    