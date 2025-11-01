import argparse
from app.services.conexion_nosql import (
  conectar_mongo,
  conectar_neo4j,
  conectar_redis,
)
from app.services.funciones import get_recommendations, clear_offer_cache, recompute_matches

def parse_args():
    p = argparse.ArgumentParser(prog="talentum-cli", description="CLI Talentum+")
    sub = p.add_subparsers(dest="cmd", required=True)

    # recomendaciones
    rec = sub.add_parser("recs", help="Obtener recomendaciones para una oferta")
    rec.add_argument("--oferta", required=True, help="ID de oferta (ej.: of-backend)")

    # recomputar
    reco = sub.add_parser("recompute", help="Recomputar recomendaciones y refrescar cache")
    reco.add_argument("--oferta", required=True)

    # invalidar cache
    inv = sub.add_parser("invalidate", help="Borrar cache de una oferta")
    inv.add_argument("--oferta", required=True)

    return p.parse_args()

def main():
    args = parse_args()
    db = conectar_mongo()
    graph = conectar_neo4j()
    r = conectar_redis()

    if any(x is None for x in (db, graph, r)):
        print("Falta alguna conexión (Mongo/Neo4j/Redis).")
        return

    if args.cmd == "recs":
        res = get_recommendations(db, graph, r, args.oferta)
        print(f"Fuente: {res['source']}")
        print("Recs:", res["recs"])
        print("Perfiles:", res["perfiles"])

    elif args.cmd == "recompute":
        items = recompute_matches(db, graph, r, args.oferta)
        print("Recomputadas:", len(items))
        print(items)

    elif args.cmd == "invalidate":
        deleted = clear_offer_cache(r, args.oferta)
        print("Eliminadas:", deleted)

if __name__ == "__main__":
    main()