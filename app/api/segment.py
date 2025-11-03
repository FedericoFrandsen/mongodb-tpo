from fastapi import APIRouter, HTTPException, Query
from app.services.conexion_nosql import conectar_mongo, conectar_redis

router = APIRouter(prefix="/segment", tags=["segment"])

@router.get("")
def segment_by_skills(skills: list[str] = Query(..., min_items=1)): #Recibe una lista de skills por query string
    r = conectar_redis()
    db = conectar_mongo()
    if r is None or db is None:
        raise HTTPException(500, "Conexiones no disponibles")
    keys = [f"skill:{s.strip().lower()}:users" for s in skills] #En Redis cada skill tiene un set de usuarios: skill:python:users. Devuelve los usuarios que tienen todos los skills (intersección de sets)
    users = r.smembers(keys[0]) if len(keys) == 1 else r.sinter(*keys)
    perfiles = list(
        db.candidatos.find(
            {"informacion_personal.nombre_apellido": {"$in": list(users)}},
            {
                "_id": 0,
                "informacion_personal.nombre_apellido": 1,
                "informacion_personal.email": 1,
                "estado": 1,
                "habilidades.tecnicas": 1,
            },
        )
    )
    #En MongoDB: Busca los perfiles de esos usuarios y devuelve campos básicos (nombre, email, estado, skills técnicas)
    return {"skills": skills, "users": list(users), "perfiles": perfiles}

    #Retorna un JSON con:
    #skills → skills buscados
    #users → nombres de los usuarios
    #perfiles → datos de los usuarios

