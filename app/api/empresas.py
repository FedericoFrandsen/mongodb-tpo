# app/api/empresas.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.services.conexion_nosql import conectar_mongo

router = APIRouter(prefix="/empresas", tags=["empresas"])


# =========================
# Modelos
# =========================
class Contacto(BaseModel):
    direccion: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None


class EmpresaIn(BaseModel):
    nombre: str
    industria: Optional[str] = None
    descripcion: Optional[str] = None
    contacto: Optional[Contacto] = None


# =========================
# Crear empresa
# =========================
@router.post("")
def create_company(e: EmpresaIn):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    nombre = e.nombre.strip()
    if not nombre:
        raise HTTPException(400, "Nombre requerido")

    exists = db.empresas.find_one({"nombre": nombre}, {"_id": 1})
    if exists:
        raise HTTPException(409, "La empresa ya existe")

    doc = {
        "nombre": nombre,
        "industria": e.industria or None,
        "descripcion": e.descripcion or None,
        "contacto": (e.contacto.dict() if e.contacto else None),
        "empleados_rrhh": None,
        "fecha_creacion": datetime.utcnow(),
    }
    ins = db.empresas.insert_one(doc)
    return {"ok": True, "empresa_id": str(ins.inserted_id), "nombre": nombre}


# =========================
# Listar empresas
# =========================
@router.get("")
def list_companies():
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")
    cur = db.empresas.find({}, {"_id": 0, "nombre": 1, "industria": 1})
    return {"empresas": list(cur)}


# =========================
# Detalle de empresa
# =========================
@router.get("/{nombre}")
def get_company(nombre: str):
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    empresa = db.empresas.find_one({"nombre": nombre}, {"_id": 0})
    if not empresa:
        raise HTTPException(404, "Empresa no encontrada")
    return {"empresa": empresa}


# =========================
# Posiciones por empresa
# =========================
@router.get("/{nombre}/positions")
def list_positions_by_company(nombre: str, estado: Optional[str] = None):
    """
    Devuelve las posiciones/ofertas de una empresa, con resumen para el dashboard.
    Permite filtrar opcionalmente por estado (?estado=abierta).
    """
    db = conectar_mongo()
    if db is None:
        raise HTTPException(500, "Conexión Mongo no disponible")

    emp = db.empresas.find_one({"nombre": nombre})
    if not emp:
        raise HTTPException(404, "Empresa no encontrada")

    filtro = {"empresa_id": emp["_id"]}
    if estado:
        filtro["estado"] = estado

    cur = db.ofertas.find(
        filtro,
        {
            "_id": 0,
            "puesto": 1,
            "descripcion": 1,
            "requerimientos": 1,
            "modalidad": 1,
            "estado": 1,
            "ubicacion": 1,
            "fecha_creacion": 1,
            "experiencia_requerida": 1,
            "estudios_requeridos": 1,
        }
    ).sort("fecha_creacion", -1)

    ofertas = []
    for o in cur:
        reqs = o.get("requerimientos", [])
        req_str = ", ".join([(r.get("habilidad") or "").strip().lower() for r in reqs])
        ofertas.append({
            "puesto": o.get("puesto", ""),
            "descripcion": o.get("descripcion", ""),
            "skills_requeridos": req_str,
            "modalidad": o.get("modalidad", "") or "",
            "ubicacion": o.get("ubicacion", "") or "",
            "estado": o.get("estado", "abierta"),
            "experiencia_minima": o.get("experiencia_requerida", "") or "",
            "estudios_requeridos": o.get("estudios_requeridos", "") or "",
            "fecha_creacion": o.get("fecha_creacion"),
        })

    return {"empresa": nombre, "ofertas": ofertas}