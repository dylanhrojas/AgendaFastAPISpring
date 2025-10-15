from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# CREATE - Crear nueva persona
def crear_persona(db: Session, persona: schemas.PersonaCreate):
    # Verificar si el email ya existe
    db_persona = db.query(models.Persona).filter(models.Persona.email == persona.email).first()
    if db_persona:
        raise ValueError("El email ya está registrado")
    
    # Crear nueva persona
    db_persona = models.Persona(
        nombre=persona.nombre,
        apellido=persona.apellido,
        email=persona.email,
        telefono=persona.telefono,
        direccion=persona.direccion
    )
    
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

# READ - Obtener persona por ID
def obtener_persona(db: Session, persona_id: int):
    return db.query(models.Persona).filter(models.Persona.id == persona_id).first()

# READ - Obtener todas las personas
def obtener_personas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Persona).offset(skip).limit(limit).all()

# READ - Obtener persona por email
def obtener_persona_por_email(db: Session, email: str):
    return db.query(models.Persona).filter(models.Persona.email == email).first()

# UPDATE - Actualizar persona
def actualizar_persona(db: Session, persona_id: int, persona: schemas.PersonaUpdate):
    db_persona = db.query(models.Persona).filter(models.Persona.id == persona_id).first()
    
    if not db_persona:
        return None
    
    # Actualizar solo los campos proporcionados
    update_data = persona.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_persona, field, value)
    
    db.commit()
    db.refresh(db_persona)
    return db_persona

# DELETE - Eliminar persona
def eliminar_persona(db: Session, persona_id: int):
    db_persona = db.query(models.Persona).filter(models.Persona.id == persona_id).first()
    
    if not db_persona:
        return None
    
    db.delete(db_persona)
    db.commit()
    return db_persona
