from pymongo import MongoClient
from py2neo import Graph
import redis

_db = None
_graph = None
_r = None
#Se usan para guardar la conexión y no volver a conectarse cada vez que se llama a la función
#Esto mejora el rendimiento y evita abrir muchas conexiones

def conectar_mongo():
    global _db
    if _db is not None:
        return _db
    try:
        client = MongoClient(
            "mongodb://admin:password123@localhost:27017/",
            authSource="admin",
        )
        _db = client["tpo_database"]
        print("Conectado a MongoDB")
    except Exception as e:
        print("Error conectando a MongoDB:", e)
        _db = None
    return _db

def conectar_neo4j():
    global _graph
    if _graph is not None:
        return _graph
    try:
        _graph = Graph("bolt://localhost:7687", auth=("neo4j", "devpass123"))
        print("Conectado a Neo4j")
    except Exception as e:
        print("Error conectando a Neo4j:", e)
        _graph = None
    return _graph

def conectar_redis():
    global _r
    if _r is not None:
        return _r
    try:
        _r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True) #decode_responses=True → convierte los datos de bytes a strings
        _r.ping()
        print("Conectado a Redis")
    except Exception as e:
        print("Error conectando a Redis:", e)
        _r = None
    return _r

if __name__ == "__main__":
    conectar_mongo()
    conectar_neo4j()
    conectar_redis()