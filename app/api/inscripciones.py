from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.services.conexion_nosql import conectar_mongo, conectar_neo4j
from app.services.versiones import log_version, get_candidato_id_by_nombre

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])


class InscripcionIn(BaseModel):
    usuario: str      # nombre del candidato (lowercase)
    curso: str        # título del curso


class ProgresoIn(BaseModel):
    usuario: str
    curso: str
    progreso: Optional[float] = None  # 0..100
    nota: Optional[float] = None
    completar: bool = False           # si True, marca como completado
    sumar_skill: bool = True          # si True, agrega la skill_asociada si la hay


@router.post("")
def inscribirse(inf: InscripcionIn):
    """
    Inscribe a un usuario en un curso (colección inscripciones).
    """
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Mongo no disponible")

    user = (inf.usuario or "").strip().lower()
    curso = (inf.curso or "").strip()

    cand = db.candidatos.find_one({"informacion_personal.nombre_apellido": user})
    if not cand:
        raise HTTPException(404, f"Usuario '{user}' no encontrado")

    c = db.cursos.find_one({"titulo": curso})
    if not c:
        raise HTTPException(404, f"Curso '{curso}' no encontrado")

    # Evitar duplicados
    exists = db.inscripciones.find_one({"candidato_id": cand["_id"], "curso_id": c["_id"]})
    if exists:
        return {"ok": True, "message": "Ya estaba inscripto"}

    doc = {
        "candidato_id": cand["_id"],
        "curso_id": c["_id"],
        "progreso": 0,
        "nota": None,
        "fecha_inicio": datetime.utcnow(),
        "fecha_fin": None,
    }
    db.inscripciones.insert_one(doc)

    # Versión en historial
    log_version(
        db,
        cand["_id"],
        cambio=f"Se inscribió al curso {curso}",
        diff={"curso": curso, "progreso": 0}
    )

    return {"ok": True, "usuario": user, "curso": curso}


@router.post("/progreso")
def actualizar_progreso(p: ProgresoIn):
    """
    Actualiza el progreso de una inscripción. Si completar=True:
      - marca fecha_fin
      - si sumar_skill y el curso tiene skill_asociada, agrega la skill al usuario
      - guarda versión en el historial
    """
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Mongo no disponible")

    user = (p.usuario or "").strip().lower()
    curso = (p.curso or "").strip()

    cand = db.candidatos.find_one({"informacion_personal.nombre_apellido": user})
    if not cand:
        raise HTTPException(404, "Usuario no encontrado")

    c = db.cursos.find_one({"titulo": curso})
    if not c:
        raise HTTPException(404, "Curso no encontrado")

    insc = db.inscripciones.find_one({"candidato_id": cand["_id"], "curso_id": c["_id"]})
    if not insc:
        raise HTTPException(404, "No hay inscripción para ese curso")

    upd = {
        "progreso": p.progreso if p.progreso is not None else insc.get("progreso", 0),
        "nota": p.nota if p.nota is not None else insc.get("nota", None),
        "fecha_fin": datetime.utcnow() if p.completar else insc.get("fecha_fin"),
    }
    db.inscripciones.update_one(
        {"_id": insc["_id"]},
        {"$set": upd}
    )

    # Si completó y el curso tiene skill_asociada, agregamos skill al usuario
    added_skill = None
    if p.completar and p.sumar_skill and (c.get("skill_asociada")):
        skill = c["skill_asociada"].strip().lower()
        db.candidatos.update_one(
            {"_id": cand["_id"]},
            {"$addToSet": {"habilidades.tecnicas": {"nombre": skill, "nivel": 5}}}
        )
        added_skill = skill

    # Registrar versión
    diff = {"curso": curso, "progreso": upd["progreso"], "nota": upd["nota"]}
    if p.completar:
        diff["completado"] = True
        if added_skill:
            diff["skill_agregada"] = added_skill

    log_version(
        db,
        cand["_id"],
        cambio=f"Actualizó progreso en curso {curso}" if not p.completar else f"Completó curso {curso}",
        diff=diff
    )

    return {
        "ok": True,
        "usuario": user,
        "curso": curso,
        "progreso": upd["progreso"],
        "nota": upd["nota"],
        "completado": p.completar,
        "skill_agregada": added_skill
    }


@router.get("/usuario/{nombre}")
def cursos_de_usuario(nombre: str):
    """
    Lista cursos (inscripciones) del usuario con progreso/nota y metadata del curso.
    """
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Mongo no disponible")

    nombre = (nombre or "").strip().lower()
    cand = db.candidatos.find_one({"informacion_personal.nombre_apellido": nombre})
    if not cand:
        raise HTTPException(404, "Usuario no encontrado")

    cur = db.inscripciones.aggregate([
        {"$match": {"candidato_id": cand["_id"]}},
        {"$lookup": {
            "from": "cursos",
            "localField": "curso_id",
            "foreignField": "_id",
            "as": "curso"
        }},
        {"$unwind": "$curso"},
        {"$project": {
            "_id": 0,
            "titulo": "$curso.titulo",
            "progreso": 1,
            "nota": 1,
            "fecha_inicio": 1,
            "fecha_fin": 1,
            "formato": "$curso.formato",
            "duracion_h": "$curso.duracion_h",
            "skill_asociada": "$curso.skill_asociada",
        }}
    ])

    return {"usuario": nombre, "cursos": list(cur)}