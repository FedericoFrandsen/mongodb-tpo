from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.services.conexion_nosql import conectar_mongo

router = APIRouter(prefix="/positions", tags=["positions"])

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