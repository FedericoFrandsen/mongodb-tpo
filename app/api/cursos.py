from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.services.conexion_nosql import conectar_neo4j

router = APIRouter(prefix="/mentoring", tags=["mentoring"])


def normalize_skill(s: str) -> str:
    return (s or "").strip().lower()


@router.get("/suggestions")
def mentoring_suggestions(user: str, skill: str, max_depth: int = 2, limit: int = 10):
    """
    Sugerir mentores en la red para un usuario y una skill objetivo.
    Busca en Neo4j usuarios conectados en 1..max_depth saltos que tengan esa skill.

    Parámetros:
      - user: nombre del usuario (lowercase)
      - skill: la skill que el usuario quiere aprender/reforzar
      - max_depth: distancia máxima en el grafo (1 o 2 recomendado)
      - limit: cantidad máxima de sugerencias

    Retorna:
      - mentores: lista de {mentor, distancia, via, score}
      - skill: skill objetivo
      - user: usuario
    """
    graph = conectar_neo4j()
    if graph is None:
        raise HTTPException(500, "Conexión Neo4j no disponible")

    user = (user or "").strip().lower()
    skill = normalize_skill(skill)

    if not user or not skill:
        raise HTTPException(400, "Parámetros 'user' y 'skill' son requeridos")

    # Cypher: Buscar usuarios conectados hasta max_depth con skill
    # Acomoda los labels/props según tu grafo:
    # - (u:Usuario {nombre:<user>})
    # - (m:Usuario)-[:TIENE]->(s:Skill {nombre:<skill>})
    # - Relación de conexión arbitraria: [:CONTACTO_CON|*1..max_depth]
    #   Podés ajustar a tus relaciones reales de networking
    query = f"""
    MATCH (u:Usuario {{nombre:$user}})
    MATCH (m:Usuario)-[:TIENE]->(s:Skill {{nombre:$skill}})
    WHERE m.nombre <> $user
    MATCH p=shortestPath((u)-[*1..{max_depth}]-(m))
    RETURN m.nombre AS mentor,
           length(p) AS distancia,
           [r IN relationships(p) | type(r)] AS via
    ORDER BY distancia ASC, mentor ASC
    LIMIT $limit
    """

    rows = graph.run(query, user=user, skill=skill, limit=limit).data()

    # Score simple: más cerca => mayor puntaje
    # Podés ponderar por centralidad, endorsements, etc.
    mentores = []
    for r in rows:
        dist = int(r.get("distancia", 999))
        score = max(1, (10 - dist))  # distancia 1 => 9 pts, dist 2 => 8, etc.
        mentores.append({
            "mentor": r.get("mentor"),
            "distancia": dist,
            "via": r.get("via", []),
            "score": score
        })

    return {"user": user, "skill": skill, "mentores": mentores}