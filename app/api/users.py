from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
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

    try:
        nombre = u.nombre.strip().lower()
        skills_norm = [s.strip().lower() for s in u.skills]

        exists = db.candidatos.find_one(
            {"informacion_personal.nombre_apellido": nombre},
            {"_id": 1},
        )
        print("EXISTS?", exists)
        if exists:
            raise HTTPException(409, "El usuario ya existe")

        doc = {
            "informacion_personal": {
                "nombre_apellido": nombre,
                "email": u.email,
                "celular": None,
                "residencia": None,
                "foto": None,
                "CV": None,
            },
            "estado": "activo",
            "fecha_creacion": datetime.utcnow(),          # BSON Date
            "fecha_ultima_actualizacion": None,
            "experiencia_laboral": [],
            "experiencia_academica": [],
            "habilidades": {
                "tecnicas": [{"nombre": s, "nivel": 5} for s in skills_norm],
                "blandas": [],
            },
            "ultimo_evento_seleccion": None,
        }
        print("DOC A INSERTAR:", doc)

        ins = db.candidatos.insert_one(doc)
        print("INSERTED _id:", ins.inserted_id)

        # Índices Redis
        for s in skills_norm:
            print("ADD SET:", f"skill:{s}:users", nombre)
            r.sadd(f"skill:{s}:users", nombre)

        # Cache perfil como JSON (strings ok)
        payload = json.dumps(
            {
                "informacion_personal": doc["informacion_personal"],
                "estado": doc["estado"],
                "habilidades": doc["habilidades"],
            },
            ensure_ascii=False,
            default=str,  # serializa datetime
        )
        print("CACHE KEY:", f"user:{nombre}")
        r.setex(f"user:{nombre}", 1800, payload)

        return {"ok": True, "user": nombre}

    except HTTPException:
        raise
    except Exception as e:
        print("ERROR create_user:", repr(e))
        raise HTTPException(500, "Error interno creando usuario")