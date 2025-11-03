from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.services.conexion_nosql import (
    conectar_mongo,
    conectar_redis,
    conectar_neo4j,
)
from app.services.versiones import (
    log_version,
    get_candidato_id_by_nombre,
)

import json


router = APIRouter(prefix="/users", tags=["users"])
#Todas las rutas de este archivo van a empezar con /users

# ----------------------------
# Modelos de request
# ----------------------------
class UserIn(BaseModel):
    nombre: str
    email: EmailStr
    skills: list[str] = []
#UserIn define cómo debe ser el JSON al crear un usuario

class CapacitacionRequest(BaseModel):
    nombre: str
    capacitacion: str
#CapacitacionRequest se usa para agregar una capacitación a un usuario

# ----------------------------
# Crear usuario
# ----------------------------
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
            "fecha_creacion": datetime.utcnow(),  # BSON Date
            "fecha_ultima_actualizacion": None,
            "experiencia_laboral": [],
            "experiencia_academica": [],
            "habilidades": {
                "tecnicas": [{"nombre": s, "nivel": 5} for s in skills_norm],
                "blandas": [],
            },
            "ultimo_evento_seleccion": None,
        }

        # Mongo
        ins = db.candidatos.insert_one(doc)
        cand_id = ins.inserted_id

        # Redis: índices por skill
        for s in skills_norm:
            r.sadd(f"skill:{s}:users", nombre)
        #Actualiza índices en Redis para búsquedas rápidas por skill

        # Cache perfil
        payload = json.dumps(
            {
                "informacion_personal": doc["informacion_personal"],
                "estado": doc["estado"],
                "habilidades": doc["habilidades"],
            },
            ensure_ascii=False,
            default=str,  # serializa datetime
        )
        r.setex(f"user:{nombre}", 1800, payload)
        #Guarda un cache del perfil en Redis por 30 minutos (setex).

        # Versionado en Mongo
        log_version(
            db,
            cand_id,
            cambio="Usuario creado",
            diff={
                "informacion_personal": doc["informacion_personal"],
                "estado": doc["estado"],
                "habilidades": doc["habilidades"],
            },
        )

        return {"ok": True, "user": nombre}

    except HTTPException:
        raise
    except Exception as e:
        print("ERROR create_user:", repr(e))
        raise HTTPException(500, "Error interno creando usuario")


# ----------------------------
# Agregar capacitación a un usuario
# ----------------------------
@router.post("/capacitacion")
def add_capacitacion(req: CapacitacionRequest):
    """
    Actualiza Mongo, crea la relación en Neo4j y registra versión.
    """
    db = conectar_mongo()
    graph = conectar_neo4j()
    if db is None or graph is None:
        raise HTTPException(500, "Conexiones no disponibles")

    nombre = req.nombre.strip().lower()
    cap = req.capacitacion.strip().lower()

    # Mongo: push de la capacitación
    users = db.candidatos
    users.update_one(
        {"informacion_personal.nombre_apellido": nombre},
        {"$push": {"capacitaciones": cap}},
    )
    # Actualiza MongoDB ($push para agregar la capacitación)

    # Neo4j: MERGE (Usuario)-[:REALIZO]->(Capacitacion)
    driver = graph  # py2neo.Graph si lo usás así
    # Si usás neo4j-driver nativo, adaptar a sesiones
    driver.run(
        """
        MERGE (u:Usuario {nombre:$nombre})
        MERGE (c:Capacitacion {nombre:$cap})
        MERGE (u)-[:REALIZO]->(c)
        """,
        nombre=nombre, cap=cap
    )

    # Versionado
    cand_id = get_candidato_id_by_nombre(db, nombre)
    if cand_id:
        log_version(
            db,
            cand_id,
            cambio=f"Agregó capacitación {cap}",
            diff={"capacitacion": cap},
        )

    return {"message": f"Capacitación '{cap}' agregada a '{nombre}'"}


# ----------------------------
# Obtener usuario por nombre
# ----------------------------
@router.get("/{nombre}")
def get_user(nombre: str):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    nombre = nombre.strip().lower()
    user = db.candidatos.find_one(
        {"informacion_personal.nombre_apellido": nombre},
        {"_id": 0}
    )
    if not user:
        return {"error": "Usuario no encontrado"}
    return user


# ----------------------------
# Eliminar usuario por nombre
# ----------------------------
@router.delete("/{nombre}")
def delete_user(nombre: str):
    db = conectar_mongo()
    r = conectar_redis()
    if db is None or r is None:
        raise HTTPException(500, "Conexiones no disponibles")

    nombre = nombre.strip().lower()
    res = db.candidatos.delete_one(
        {"informacion_personal.nombre_apellido": nombre}
    )
    # Opcional: limpiar índices de Redis (si lo querés)
    # Podrías recorrer sus skills primero y hacer SREM por cada skill.
    r.delete(f"user:{nombre}")
    return {"deleted": res.deleted_count}


# ----------------------------
# Historial de versiones del usuario
# ----------------------------
@router.get("/{nombre}/versiones")
def get_versiones(nombre: str):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    cand_id = get_candidato_id_by_nombre(db, nombre)
    if not cand_id:
        raise HTTPException(404, "Usuario no encontrado")

    cur = db.versiones_perfil.find(
        {"candidato_id": cand_id},
        {"_id": 0, "candidato_id": 0},
    ).sort("version", 1)
    return {"nombre": nombre, "versiones": list(cur)}

#Busca el ID del candidato en MongoDB
#Recupera el historial de versiones de la colección versiones_perfil
#Devuelve un JSON con todas las versiones ordenadas por número de versión

#Resumen
# 1) Crear usuario → MongoDB + Redis + versionado
# 2) Agregar capacitación → MongoDB + Neo4j + versionado
# 3) Obtener usuario → MongoDB
# 4) Eliminar usuario → MongoDB + Redis
# 5) Historial → MongoDB