from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.conexion_nosql import conectar_mongo, conectar_redis
import json

router = APIRouter(prefix="/users", tags=["users"])

class UserIn(BaseModel):
    nombre: str
    email: EmailStr
    skills: list[str] = []

@router.post("")
def create_user(u: UserIn):
    db = conectar_mongo()
    r = conectar_redis()
    if db is None or r is None:
        raise HTTPException(500, "Conexiones no disponibles")

    nombre = u.nombre.strip().lower()
    skills_norm = [s.strip().lower() for s in u.skills]

    # opcional: evitar duplicados
    exists = db.candidatos.find_one(
        {"informacion_personal.nombre_apellido": nombre},
        {"_id": 1},
    )
    if exists:
        raise HTTPException(409, "El usuario ya existe")

    doc = {
        "informacion_personal": {"nombre_apellido": nombre, "email": u.email},
        "estado": "activo",
        "habilidades": {
            "tecnicas": [{"nombre": s, "nivel": 5} for s in skills_norm]
        },
    }

    db.candidatos.insert_one(doc)

    for s in skills_norm:
        r.sadd(f"skill:{s}:users", nombre)

    r.setex(f"user:{nombre}", 1800, json.dumps(doc, ensure_ascii=False))

    return {"ok": True, "user": nombre}