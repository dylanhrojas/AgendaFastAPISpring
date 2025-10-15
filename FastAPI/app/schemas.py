from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Esquema base
class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None

# Esquema para crear persona
class PersonaCreate(PersonaBase):
    pass

# Esquema para actualizar persona
class PersonaUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

# Esquema para respuesta (incluye campos automáticos)
class Persona(PersonaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Reemplaza 'orm_mode = True' en Pydantic v2
