from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List

from app.services.conexion_nosql import (
    conectar_mongo,
    conectar_redis,
    conectar_neo4j,
)
from app.services.versiones import (
    log_version,
    get_candidato_id_by_nombre,
)

router = APIRouter(prefix="/skills", tags=["skills"])


# ----------------------------
# Modelos
# ----------------------------
class AddSkillIn(BaseModel):
    user: str
    skill: str
    nivel: int = 5  # valor por defecto 

class SkillsRequest(BaseModel):
    skills: List[str]


# ----------------------------
# Agregar skill a un usuario
# ----------------------------
@router.post("/add")
def add_skill(body: AddSkillIn):
    """
    - MongoDB: agrega una habilidad y su nivel. Inserta un registro en versiones_perfil
    - Redis: agrega al set skill:{skill}:users
    """
    db = conectar_mongo()
    r = conectar_redis()

    user = body.user.strip().lower()
    skill = body.skill.strip().lower()

    # Mongo: $addToSet para evitar duplicados
    res = db.candidatos.update_one(
    {
        "informacion_personal.nombre_apellido": {
            "$regex": f"^{user}$",
            "$options": "i"  # i = insensible a mayúsculas/minúsculas
        }
    },
    {
        "$addToSet": {
            "habilidades.tecnicas": {"nombre": skill, "nivel": body.nivel}
        }
    },
    )
    if res.matched_count == 0:
        raise HTTPException(404, f"Usuario '{user}' no encontrado")

    # Redis: índice por skill
    r.sadd(f"skill:{skill}:users", user)

    # Invalida cache de perfil (opcional si lo usás)
    r.delete(f"user:{user}")

    # Versionado
    cand_id = get_candidato_id_by_nombre(db, user)
    if cand_id:
        log_version(
            db,
            cand_id,
            cambio=f"Agregó skill {skill}",
            diff={"skills": [{"nombre": skill, "nivel": body.nivel}]},
        )

    return {"ok": True, "user": user, "skill": skill}


# -------------------------------
# Segmentación por skills (Redis)
# -------------------------------
@router.get("/segment")
def segment_by_skills(skills: List[str] = Query(..., min_items=1)):
    """
    Segmenta usuarios por intersección de skills usando Redis sets:
      - SINTER skill:{s1}:users skill:{s2}:users ...
    Luego enriquece perfiles desde Mongo.
    """
    r = conectar_redis()
    db = conectar_mongo()
    if r is None or db is None:
        raise HTTPException(500, "Conexiones no disponibles")

    skills_norm = [s.strip().lower() for s in skills if s.strip()]
    if not skills_norm:
        raise HTTPException(400, "Debe proveer al menos un skill")

    keys = [f"skill:{s}:users" for s in skills_norm] 
    #Cada skill tiene un set en Redis que contiene los usuarios que la tienen
    #skill:python:users = { "trinidad echevarria", "rosario martinez" }
    if len(keys) == 1:
        users = r.smembers(keys[0])
    else:
        users = r.sinter(*keys)

    users = list(users or [])
    # Enriquecimiento desde Mongo
    perfiles = list(
        db.candidatos.find(
            {"informacion_personal.nombre_apellido": {"$in": users}},
            {
                "_id": 0,
                "informacion_personal": 1,
                "estado": 1,
                "habilidades.tecnicas": 1,
            },
        )
    )
    return {"skills": skills_norm, "users": users, "perfiles": perfiles}

