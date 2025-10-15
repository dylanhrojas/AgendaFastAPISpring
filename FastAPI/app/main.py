from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from .spring_client import SpringAPIClient

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="API Agenda de Contactos",
    description="Una API REST para gestionar una agenda de contactos",
    version="1.0.0"
)

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Cliente Spring API
spring_client = SpringAPIClient()

# Raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Agenda de Contactos"}

# CREATE - Crear nueva persona
@app.post("/personas/", response_model=schemas.Persona, status_code=status.HTTP_201_CREATED)
async def crear_persona(persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    try:
        # Guardar en FastAPI
        db_persona = crud.crear_persona(db=db, persona=persona)

        # Sincronizar con Spring Boot
        persona_dict = {
            "nombre": db_persona.nombre,
            "apellido": db_persona.apellido,
            "email": db_persona.email,
            "telefono": db_persona.telefono,
            "direccion": db_persona.direccion
        }
        await spring_client.crear_persona(persona_dict)

        return db_persona
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# READ - Obtener todas las personas
@app.get("/personas/", response_model=List[schemas.Persona])
def leer_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    personas = crud.obtener_personas(db, skip=skip, limit=limit)
    return personas

# READ - Obtener persona por ID
@app.get("/personas/{persona_id}", response_model=schemas.Persona)
def leer_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = crud.obtener_persona(db, persona_id=persona_id)
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    return db_persona

# UPDATE - Actualizar persona
@app.put("/personas/{persona_id}", response_model=schemas.Persona)
async def actualizar_persona(persona_id: int, persona: schemas.PersonaUpdate, db: Session = Depends(get_db)):
    db_persona = crud.actualizar_persona(db, persona_id=persona_id, persona=persona)
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )

    # NO sincronizamos actualizaciones porque los IDs no coinciden entre bases de datos
    # Solo sincronizamos creaciones nuevas

    return db_persona

# DELETE - Eliminar persona
@app.delete("/personas/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = crud.eliminar_persona(db, persona_id=persona_id)
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )

    # NO sincronizamos eliminaciones porque los IDs no coinciden entre bases de datos

    return None

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}


# ========== RUTAS WEB (HTML) ==========

# Página principal - Lista de personas
@app.get("/web/", response_class=HTMLResponse)
def web_index(request: Request, db: Session = Depends(get_db)):
    personas = crud.obtener_personas(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "personas": personas
    })

# Mostrar formulario para crear nueva persona
@app.get("/web/nuevo", response_class=HTMLResponse)
def web_nuevo(request: Request):
    return templates.TemplateResponse("formulario.html", {
        "request": request,
        "persona": None,
        "accion": "Crear"
    })

# Procesar creación de nueva persona
@app.post("/web/guardar")
async def web_guardar(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        persona_data = schemas.PersonaCreate(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion
        )
        # Guardar en FastAPI
        db_persona = crud.crear_persona(db=db, persona=persona_data)

        # Sincronizar con Spring Boot
        persona_dict = {
            "nombre": db_persona.nombre,
            "apellido": db_persona.apellido,
            "email": db_persona.email,
            "telefono": db_persona.telefono,
            "direccion": db_persona.direccion
        }
        await spring_client.crear_persona(persona_dict)

        return RedirectResponse(url="/web/", status_code=303)
    except ValueError as e:
        personas = crud.obtener_personas(db)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "personas": personas,
            "error": str(e)
        })

# Mostrar formulario para editar persona
@app.get("/web/editar/{persona_id}", response_class=HTMLResponse)
def web_editar(request: Request, persona_id: int, db: Session = Depends(get_db)):
    persona = crud.obtener_persona(db, persona_id)
    if not persona:
        return RedirectResponse(url="/web/", status_code=303)
    return templates.TemplateResponse("formulario.html", {
        "request": request,
        "persona": persona,
        "accion": "Editar"
    })

# Procesar actualización de persona
@app.post("/web/actualizar/{persona_id}")
async def web_actualizar(
    request: Request,
    persona_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    persona_data = schemas.PersonaUpdate(
        nombre=nombre,
        apellido=apellido,
        email=email,
        telefono=telefono,
        direccion=direccion
    )
    crud.actualizar_persona(db, persona_id, persona_data)

    # NO sincronizamos actualizaciones porque los IDs no coinciden

    return RedirectResponse(url="/web/", status_code=303)

# Eliminar persona
@app.get("/web/eliminar/{persona_id}")
async def web_eliminar(persona_id: int, db: Session = Depends(get_db)):
    crud.eliminar_persona(db, persona_id)

    # NO sincronizamos eliminaciones porque los IDs no coinciden

    return RedirectResponse(url="/web/", status_code=303)

# Ver detalles de persona
@app.get("/web/ver/{persona_id}", response_class=HTMLResponse)
def web_ver(request: Request, persona_id: int, db: Session = Depends(get_db)):
    persona = crud.obtener_persona(db, persona_id)
    if not persona:
        return RedirectResponse(url="/web/", status_code=303)
    return templates.TemplateResponse("detalle.html", {
        "request": request,
        "persona": persona
    })


# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
