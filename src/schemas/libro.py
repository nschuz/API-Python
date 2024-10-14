from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class LibroSchema(BaseModel):
    id: int
    titulo: str
    fecha_publicacion: date
    autor_id: int
    
    class Config:
        from_attributes=True
        orm_mode=True
        

class LibrosSchemaRequest(BaseModel):
    
    titulo: Optional[str]
    fecha_publicacion: Optional[date]
    autor_id: Optional[int]
    
