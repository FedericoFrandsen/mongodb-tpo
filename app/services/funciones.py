from typing import Iterable, List, Dict, Tuple
from pymongo.database import Database
from py2neo import Graph
import redis

TTL_MATCH_SECONDS = 900  # 15 minutos


def _puesto_por_oferta_id(oferta_id: str) -> str:
    """
    Mapea los IDs simbólicos de oferta a un 'puesto' exacto en Mongo.
    """
    mapa = {
        "of-backend": "Desarrollador Backend",
        "of-analista-datos": "Analista de Datos",
        "of-especialista-ia": "Especialista en IA",
    }
    return mapa.get(oferta_id, "")


def enrich_from_mongo(db: Database, candidatos_por_nombre: Iterable[str]) -> List[Dict]:
    """
    Devuelve perfiles compactos desde Mongo por nombre (nombre_apellido).
    """
    if db is None or not candidatos_por_nombre:
        return []
    cur = db.candidatos.find(
        {
            "informacion_personal.nombre_apellido": {
                "$in": list(set(candidatos_por_nombre))
            }
        },
        {
            "_id": 0,
            "informacion_personal.nombre_apellido": 1,
            "informacion_personal.email": 1,
            "estado": 1,
            "habilidades.tecnicas": 1,
        },
    )
    return list(cur)


def explain_match(cand_doc: Dict, requerimientos: List[str]) -> Dict:
    """
    Calcula coincidencias y puntaje SIN equivalencias:
      - Coincidencia exacta de strings (req == skill).
      - Score = suma(10 + nivel) por cada requerimiento presente; mínimo 1 si no hay match.
    """
    skills = {
        s.get("nombre"): int(s.get("nivel", 0))
        for s in (cand_doc.get("habilidades", {}).get("tecnicas", []) or [])
    }
    matches = []
    for req in (requerimientos or []):
        if req in skills:
            matches.append(
                {"skill": req, "nivel": skills[req], "puntos": 10 + skills[req]}
            )
    total = sum(m["puntos"] for m in matches) or 1
    return {"matches": matches, "total": total}


def _buscar_oferta_en_mongo(db: Database, oferta_id: str) -> Dict:
    """
    Busca la oferta en Mongo por el 'puesto' exacto según el ID simbólico.
    """
    if db is None or not oferta_id:
        return {}
    puesto = _puesto_por_oferta_id(oferta_id)
    if not puesto:
        return {}
    return db.ofertas.find_one({"puesto": puesto}) or {}


def recompute_matches(
    db: Database, graph: Graph, r: redis.Redis, oferta_id: str
) -> List[Tuple[str, float]]:
    """
    Calcula afinidad para una oferta y escribe el ZSET en Redis.
    Retorna [(nombre, score)].
    """
    # 1) Requerimientos de la oferta desde Mongo (por puesto exacto)
    oferta = _buscar_oferta_en_mongo(db, oferta_id)
    reqs = [x.get("habilidad") for x in (oferta.get("requerimientos") or [])]
    reqs = [x for x in reqs if x]

    # 2) Candidatos postulados a esa oferta en Neo4j (por nombre)
    rows = graph.run(
        """
        MATCH (c:Candidato)-[:POSTULA_A]->(o:Oferta {id:$ofid})
        RETURN DISTINCT c.nombre AS nombre
        UNION
        MATCH (c:Candidato)-[:POSTULO_A]->(o:Oferta {id:$ofid})
        RETURN DISTINCT c.nombre AS nombre
        """,
        ofid=oferta_id,
    ).data()
    cand_nombres = [row["nombre"] for row in rows]

    # 3) Enriquecimiento Mongo
    perfiles = enrich_from_mongo(db, cand_nombres)

    # 4) Calcular score y cargar Redis
    zkey = f"cache:match:{oferta_id}"
    r.delete(zkey)
    resultados: List[Tuple[str, float]] = []
    for p in perfiles:
        nombre = p["informacion_personal"]["nombre_apellido"]
        info = explain_match(p, reqs)
        s = float(info["total"])  # mínimo 1 si no hay matches
        resultados.append((nombre, s))
    if resultados:
        r.zadd(zkey, dict(resultados))
        r.expire(zkey, TTL_MATCH_SECONDS)
    return resultados


def get_recommendations(
    db: Database, graph: Graph, r: redis.Redis, oferta_id: str
) -> Dict:
    """
    Fast-path: leer desde Redis. Si no hay, usar lock, recalcular (Neo4j+Mongo),
    poblar Redis y devolver.
    """
    zkey = f"cache:match:{oferta_id}"
    recs = r.zrange(zkey, 0, -1, withscores=True)
    if recs:
        nombres = [n for (n, _s) in recs]
        perfiles = enrich_from_mongo(db, nombres)
        return {"source": "redis", "recs": recs, "perfiles": perfiles}

    lock_key = f"lock:match:{oferta_id}"
    locked = r.set(lock_key, "worker", nx=True, ex=10)
    if locked:
        resultados = recompute_matches(db, graph, r, oferta_id)
        perfiles = enrich_from_mongo(db, [n for (n, _s) in resultados])
        return {"source": "recomputed", "recs": resultados, "perfiles": perfiles}

    import time

    time.sleep(2)
    recs = r.zrange(zkey, 0, -1, withscores=True)
    nombres = [n for (n, _s) in recs]
    perfiles = enrich_from_mongo(db, nombres)
    return {"source": "delayed-redis", "recs": recs, "perfiles": perfiles}


def clear_offer_cache(r: redis.Redis, oferta_id: str) -> int:
    """
    Elimina el ZSET de recomendaciones de una oferta en Redis.
    Retorna 1 si lo borró, 0 si no existía o si r es None.
    """
    if r is None or not oferta_id:
        return 0
    return r.delete(f"cache:match:{oferta_id}")