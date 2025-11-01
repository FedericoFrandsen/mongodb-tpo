# app/services/versiones.py
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pymongo.database import Database


def _get_next_version(db: Database, candidato_id: ObjectId) -> int:
    """
    Obtiene el siguiente número de versión para un candidato.
    Busca la última versión y retorna +1. Si no hay, retorna 1.
    """
    doc = db.versiones_perfil.find_one(
        {"candidato_id": candidato_id},
        sort=[("version", -1)],
        projection={"version": 1},
    )
    if not doc:
        return 1
    return int(doc.get("version", 0)) + 1


def log_version(
    db: Database,
    candidato_id: ObjectId | str,
    cambio: str,
    diff: Optional[dict] = None,
) -> dict:
    """
    Inserta una versión en la colección versiones_perfil.

    Parámetros:
      - db: instancia Database (pymongo)
      - candidato_id: ObjectId (o string convertible) del candidato
      - cambio: descripción corta del cambio ("Usuario creado", "Agregó skill fastapi", etc.)
      - diff: diccionario con el detalle del cambio (estructura libre)

    Retorna el documento insertado (sin _id).
    """
    # Normalizar a ObjectId si viene string
    if not isinstance(candidato_id, ObjectId):
        try:
            candidato_id = ObjectId(str(candidato_id))
        except Exception as e:
            raise ValueError(f"candidato_id inválido: {e}")

    version = _get_next_version(db, candidato_id)

    doc = {
        "candidato_id": candidato_id,
        "version": version,
        "fecha": datetime.utcnow(),
        "cambio": cambio,
        "diff": diff or None,
    }

    db.versiones_perfil.insert_one(doc)
    # Retornar sin _id para respuestas limpias
    return {
        "candidato_id": str(candidato_id),
        "version": version,
        "fecha": doc["fecha"].isoformat(),
        "cambio": cambio,
        "diff": diff or None,
    }


def get_candidato_id_by_nombre(db: Database, nombre: str) -> ObjectId | None:
    """
    Busca el _id del candidato por informacion_personal.nombre_apellido (normalizado a lowercase).
    Retorna ObjectId o None si no existe.
    """
    nombre = (nombre or "").strip().lower()
    doc = db.candidatos.find_one(
        {"informacion_personal.nombre_apellido": nombre},
        {"_id": 1},
    )
    return doc["_id"] if doc else None