from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from app.services.conexion_nosql import conectar_mongo

router = APIRouter(prefix="/posiciones", tags=["posiciones"])


# ----------------------------
# Modelos
# ----------------------------
class ReqItem(BaseModel):
    habilidad: str
    nivel: int


class PositionIn(BaseModel):
    empresa: str
    puesto: str
    descripcion: Optional[str] = None
    requerimientos: List[ReqItem]
    ubicacion: Optional[str] = None
    modalidad: Optional[str] = None   # "presencial", "remoto", "híbrido"
    estado: Optional[str] = "abierta"
    experiencia_requerida: Optional[str] = None   # string "1", "2", etc
    estudios_requeridos: Optional[str] = None     # ej. "universitario"


class PositionUpdate(BaseModel):
    puesto: Optional[str] = None
    descripcion: Optional[str] = None
    requerimientos: Optional[List[ReqItem]] = None
    ubicacion: Optional[str] = None
    modalidad: Optional[str] = None
    estado: Optional[str] = None
    experiencia_requerida: Optional[str] = None
    estudios_requeridos: Optional[str] = None


def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(400, "ID inválido")


# ----------------------------
# Crear posición (tu endpoint)
# ----------------------------
@router.post("")
def create_position(p: PositionIn):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    empresa = db.empresas.find_one({"nombre": p.empresa})
    if not empresa:
        raise HTTPException(404, f"Empresa '{p.empresa}' no encontrada")

    reqs = []
    for r in p.requerimientos:
        skill = r.habilidad.strip()
        nivel = int(r.nivel)
        if not skill or nivel < 0:
            raise HTTPException(400, "Requerimiento inválido")
        reqs.append({"habilidad": skill, "nivel": nivel})

    doc = {
        "empresa_id": empresa["_id"],
        "puesto": p.puesto.strip(),
        "descripcion": p.descripcion or None,
        "requerimientos": reqs,
        "ubicacion": p.ubicacion or None,
        "modalidad": p.modalidad or None,
        "estado": p.estado or "abierta",
        "fecha_creacion": datetime.utcnow(),
        # extras opcionales para dashboard:
        "experiencia_requerida": p.experiencia_requerida or None,
        "estudios_requeridos": p.estudios_requeridos or None,
    }
    ins = db.ofertas.insert_one(doc)
    return {"ok": True, "oferta_id": str(ins.inserted_id), "puesto": p.puesto}


# ----------------------------
# Listar posiciones (con filtros opcionales)
# ----------------------------
@router.get("")
def list_positions(
    empresa: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    puesto: Optional[str] = Query(None),
):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    filtro = {}
    if empresa:
        emp = db.empresas.find_one({"nombre": empresa}, {"_id": 1})
        if not emp:
            return {"positions": []}
        filtro["empresa_id"] = emp["_id"]
    if estado:
        filtro["estado"] = estado
    if puesto:
        filtro["puesto"] = {"$regex": puesto, "$options": "i"}

    cur = db.ofertas.find(
        filtro,
        {
            "_id": 1,
            "empresa_id": 1,
            "puesto": 1,
            "descripcion": 1,
            "requerimientos": 1,
            "estado": 1,
            "modalidad": 1,
            "ubicacion": 1,
            "fecha_creacion": 1,
            "experiencia_requerida": 1,
            "estudios_requeridos": 1,
        }
    ).sort("fecha_creacion", -1)

    result = []
    for o in cur:
        empresa_doc = db.empresas.find_one({"_id": o["empresa_id"]}, {"nombre": 1}) or {}
        result.append({
            "id": str(o["_id"]),
            "empresa": empresa_doc.get("nombre", ""),
            "puesto": o.get("puesto", ""),
            "descripcion": o.get("descripcion", ""),
            "requerimientos": o.get("requerimientos", []),
            "estado": o.get("estado", ""),
            "modalidad": o.get("modalidad", ""),
            "ubicacion": o.get("ubicacion", ""),
            "experiencia_requerida": o.get("experiencia_requerida", ""),
            "estudios_requeridos": o.get("estudios_requeridos", ""),
            "fecha_creacion": o.get("fecha_creacion"),
        })

    return {"positions": result}


# ----------------------------
# Detalle de posición por ID
# ----------------------------
@router.get("/{id}")
def get_position(id: str):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    _id = to_object_id(id)
    o = db.ofertas.find_one({"_id": _id})
    if not o:
        raise HTTPException(404, "Posición no encontrada")

    empresa_doc = db.empresas.find_one({"_id": o["empresa_id"]}, {"nombre": 1}) or {}
    return {
        "id": str(o["_id"]),
        "empresa": empresa_doc.get("nombre", ""),
        "puesto": o.get("puesto", ""),
        "descripcion": o.get("descripcion", ""),
        "requerimientos": o.get("requerimientos", []),
        "estado": o.get("estado", ""),
        "modalidad": o.get("modalidad", ""),
        "ubicacion": o.get("ubicacion", ""),
        "experiencia_requerida": o.get("experiencia_requerida", ""),
        "estudios_requeridos": o.get("estudios_requeridos", ""),
        "fecha_creacion": o.get("fecha_creacion"),
    }


# ----------------------------
# Actualizar posición por ID
# ----------------------------
@router.put("/{id}")
def update_position(id: str, data: PositionUpdate):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    _id = to_object_id(id)
    set_doc = {}
    if data.puesto is not None:
        set_doc["puesto"] = data.puesto.strip()
    if data.descripcion is not None:
        set_doc["descripcion"] = data.descripcion.strip()
    if data.requerimientos is not None:
        reqs = []
        for r in data.requerimientos:
            skill = (r.habilidad or "").strip()
            nivel = int(r.nivel)
            if skill and nivel >= 0:
                reqs.append({"habilidad": skill, "nivel": nivel})
        set_doc["requerimientos"] = reqs
    if data.ubicacion is not None:
        set_doc["ubicacion"] = data.ubicacion.strip() if data.ubicacion else None
    if data.modalidad is not None:
        set_doc["modalidad"] = data.modalidad.strip() if data.modalidad else None
    if data.estado is not None:
        set_doc["estado"] = data.estado.strip()
    if data.experiencia_requerida is not None:
        set_doc["experiencia_requerida"] = data.experiencia_requerida.strip() if data.experiencia_requerida else None
    if data.estudios_requeridos is not None:
        set_doc["estudios_requeridos"] = data.estudios_requeridos.strip() if data.estudios_requeridos else None

    if not set_doc:
        return {"ok": True, "updated": 0}

    res = db.ofertas.update_one({"_id": _id}, {"$set": set_doc})
    return {"ok": True, "updated": res.modified_count}


# ----------------------------
# Eliminar posición por ID
# ----------------------------
@router.delete("/{id}")
def delete_position(id: str):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    _id = to_object_id(id)
    res = db.ofertas.delete_one({"_id": _id})
    return {"ok": True, "deleted": res.deleted_count}