from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.conexion_nosql import conectar_mongo, conectar_redis

router = APIRouter(prefix="/skills", tags=["skills"])

class AddSkillIn(BaseModel):
    user: str
    skill: str

@router.post("/add")
def add_skill(body: AddSkillIn):
    db = conectar_mongo()
    r = conectar_redis()
    if db is None or r is None:
        raise HTTPException(500, "Conexiones no disponibles")
    user = body.user.strip().lower()
    skill = body.skill.strip().lower()
    db.candidatos.update_one(
        {"informacion_personal.nombre_apellido": user},
        {"$addToSet": {"habilidades.tecnicas": {"nombre": skill, "nivel": 5}}},
        upsert=False,
    )
    r.sadd(f"skill:{skill}:users", user)
    r.delete(f"user:{user}")
    return {"ok": True}