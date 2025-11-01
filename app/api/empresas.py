from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.services.conexion_nosql import conectar_mongo

router = APIRouter(prefix="/companies", tags=["companies"])

class Contacto(BaseModel):
    direccion: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class EmpresaIn(BaseModel):
    nombre: str
    industria: Optional[str] = None
    descripcion: Optional[str] = None
    contacto: Optional[Contacto] = None

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