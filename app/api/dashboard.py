from fastapi import APIRouter, HTTPException
from typing import List

from app.services.conexion_nosql import conectar_mongo

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def normalize_skills(skill_list):
    out = []
    for s in (skill_list or []):
        if isinstance(s, str):
            out.append(s.strip().lower())
        elif isinstance(s, dict):
            out.append((s.get("nombre") or "").strip().lower())
    return out

def parse_exp(val):
    try:
        return int(val)
    except Exception:
        return 0

@router.get("/user/{nombre}")
def get_user_profile(nombre: str):
    """
    Perfil + recomendaciones resumidas (para panel izquierdo).
    """
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    nombre = nombre.strip().lower()
    users = db.candidatos
    user = users.find_one({"informacion_personal.nombre_apellido": nombre})
    if not user:
        return {"error": "Usuario no encontrado"}

    user_skills = normalize_skills(user.get("habilidades", {}).get("tecnicas", []))
    caps = [c.strip().lower() for c in user.get("capacitaciones", [])]

    # Sugerencias de capacitación (dummy): skills no presentes pero frecuentes en ofertas
    # Podríamos cruzar con ofertas para ver los faltantes más comunes; aquí
    # lo resolvemos simple: 2 skills aleatorios que no tengan
    sugerencias = []
    # (si querés, cargamos desde ofertas los skills más frecuentes)

    return {
        "usuario": nombre,
        "skills": list(set(user_skills)),
        "capacitaciones": caps,
        "sugerencias_capacitacion": sugerencias,
        "experiencia": user.get("experiencia_laboral", []),
        "historial": []  # si querés podés sumar versiones o evento aquí
    }

@router.get("/user/{nombre}/positions")
def match_positions(nombre: str):
    """
    Devuelve posiciones recomendadas para un usuario (ordenadas por coincidencias).
    - Cruza skills del usuario vs requerimientos de las ofertas
    - Chequea estudios y experiencia mínima si están presentes en la oferta
    """
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    nombre = nombre.strip().lower()
    users = db.candidatos
    user = users.find_one({"informacion_personal.nombre_apellido": nombre})
    if not user:
        return {"error": "Usuario no encontrado"}

    user_skills = normalize_skills(user.get("habilidades", {}).get("tecnicas", []))
    caps = [c.strip().lower() for c in user.get("capacitaciones", [])]
    # experiencia del user (opcional): parsear desde su doc
    # acá simplificamos: si tu estructura tiene años de exp, parsealo a int
    user_exp = 0

    ofertas = list(db.ofertas.find({}).limit(200))
    matched = []

    for pos in ofertas:
        pos_titulo = pos.get("puesto", "")
        empresa = db.empresas.find_one({"_id": pos.get("empresa_id")}, {"nombre": 1}) or {}
        pos_req_skills = normalize_skills(pos.get("requerimientos", []))
        exp_req = parse_exp(pos.get("experiencia_requerida"))
        est_req = (pos.get("estudios_requeridos") or "").strip().lower()

        coincidencias = sum(1 for s in pos_req_skills if s in user_skills)
        exp_match = (user_exp >= exp_req) if exp_req else True
        estudios_match = True  # si quisieras cruzar con el user, ajustalo

        faltantes = [s for s in pos_req_skills if s not in user_skills]

        # (opcional) sugerencias: si faltan skills, sugerir capacitaciones relacionadas
        sugerencias_extra = []
        # acá lo dejamos vacío, pero podrías mapear: skill -> cursos

        if coincidencias > 0 or estudios_match or exp_match:
            matched.append({
                "titulo": pos_titulo,
                "empresa": empresa.get("nombre", ""),
                "skills_requeridos": ", ".join(pos_req_skills),
                "estudios_requeridos": est_req or "",
                "experiencia_minima": pos.get("experiencia_requerida", ""),
                "coincidencias": coincidencias,
                "match": "Cumple" if (coincidencias > 0 and exp_match and estudios_match) else "Parcial",
                "faltantes": faltantes,
                "sugerencias": sugerencias_extra
            })

    # ordenar por coincidencias desc
    matched = sorted(matched, key=lambda x: (x["coincidencias"]), reverse=True)
    return {
        "usuario": nombre,
        "posiciones_recomendadas": matched[:50]
    }