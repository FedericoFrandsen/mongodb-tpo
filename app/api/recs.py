from fastapi import APIRouter, HTTPException
from app.services.conexion_nosql import (
    conectar_mongo, conectar_neo4j, conectar_redis,
)
from app.services.funciones import (
    get_recommendations, recompute_matches, clear_offer_cache,
)

router = APIRouter(prefix="/offers", tags=["recommendations"])

@router.get("/{oferta_id}/recommendations")
def recommendations(oferta_id: str):
    db, graph, r = conectar_mongo(), conectar_neo4j(), conectar_redis()
    if any(x is None for x in (db, graph, r)):
        raise HTTPException(500, "Conexiones no disponibles")
    return get_recommendations(db, graph, r, oferta_id)

@router.post("/{oferta_id}/recompute")
def recompute(oferta_id: str):
    db, graph, r = conectar_mongo(), conectar_neo4j(), conectar_redis()
    if any(x is None for x in (db, graph, r)):
        raise HTTPException(500, "Conexiones no disponibles")
    items = recompute_matches(db, graph, r, oferta_id)
    return {"count": len(items), "items": items}

@router.delete("/{oferta_id}/cache")
def invalidate(oferta_id: str):
    r = conectar_redis()
    if r is None:
        raise HTTPException(500, "Redis no disponible")
    deleted = clear_offer_cache(r, oferta_id)
    return {"deleted": deleted}