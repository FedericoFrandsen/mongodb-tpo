# main.py
import argparse
from conexion_nosql import conectar_mongo, conectar_neo4j, conectar_redis
from funciones import get_recommendations

def parse_args():
    p = argparse.ArgumentParser(description="Runner Talentum+")
    p.add_argument("--oferta", default="of-backend", help="ID de oferta (ej.: of-backend)")
    return p.parse_args()

def main():
    args = parse_args()
    db = conectar_mongo()
    graph = conectar_neo4j()
    r = conectar_redis()

    # IMPORTANTE: comparar explícitamente con None (PyMongo no soporta truthy)
    if any(x is None for x in (db, graph, r)):
        print("Falta alguna conexión (Mongo/Neo4j/Redis).")
        return

    result = get_recommendations(db, graph, r, args.oferta)
    print(f"Fuente: {result['source']}")
    print("Recomendaciones:", result["recs"])
    print("Perfiles:", result["perfiles"])

if __name__ == "__main__":
    main()