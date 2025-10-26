from pymongo import MongoClient
from py2neo import Graph
import redis


def conectar_mongo():
    try:
        client = MongoClient(
            "mongodb://admin:password123@localhost:27017/",
            authSource="admin"
        )
        db = client["tpo_database"]
        print("Conectado a MongoDB")
        return db
    except Exception as e:
        print("Error conectando a MongoDB:", e)
        return None


def conectar_neo4j():
    try:
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "devpass123"))
        print("Conectado a Neo4j")
        return graph
    except Exception as e:
        print("Error conectando a Neo4j:", e)
        return None


def conectar_redis():
    try:
        r = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True  # <- clave: devuelve strings en lugar de bytes
        )
        r.ping()
        print("Conectado a Redis")
        return r
    except Exception as e:
        print("Error conectando a Redis:", e)
        return None

if __name__ == "__main__":
    conectar_mongo()
    conectar_neo4j()
    conectar_redis()