from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.services.conexion_nosql import conectar_mongo

router = APIRouter(prefix="/cursos", tags=["cursos"])


class CursoIn(BaseModel):
    titulo: str
    formato: Optional[str] = None   # "video", "pdf", "live"
    duracion_h: Optional[float] = None
    etiquetas: Optional[str] = None
    contenido_url: Optional[str] = None
    skill_asociada: Optional[str] = None  # para sumar skill al completarlo (opcional)


@router.post("")
def crear_curso(c: CursoIn):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Mongo no disponible")

    titulo = (c.titulo or "").strip()
    if not titulo:
        raise HTTPException(400, "Título requerido")

    exists = db.cursos.find_one({"titulo": titulo}, {"_id": 1})
    if exists:
        raise HTTPException(409, "Ya existe un curso con ese título")

    doc = {
        "titulo": titulo,
        "formato": c.formato or None,
        "duracion_h": c.duracion_h,
        "etiquetas": c.etiquetas or None,
        "contenido_url": c.contenido_url or None,
        "skill_asociada": (c.skill_asociada or "").strip().lower() or None,
    }
    ins = db.cursos.insert_one(doc)
    return {"ok": True, "curso_id": str(ins.inserted_id), "titulo": titulo}


@router.get("")
def listar_cursos():
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Mongo no disponible")

    cur = db.cursos.find({}, {"_id": 0})
    return {"cursos": list(cur)}


@router.get("/{titulo}")
def detalle_curso(titulo: str):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Mongo no disponible")
    c = db.cursos.find_one({"titulo": titulo}, {"_id": 0})
    if not c:
        raise HTTPException(404, "Curso no encontrado")
    return {"curso": c}