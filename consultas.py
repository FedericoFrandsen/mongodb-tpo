from conexion_nosql import conectar_mongo, conectar_neo4j, conectar_redis


# Conexiones
db = conectar_mongo()
graph = conectar_neo4j()
r = conectar_redis() 


# ----------------------------
# Consultas MONGODB
# ----------------------------
if db is not None:
    print("\nDatos en MongoDB (colección candidatos):")
    try:
        for doc in db["candidatos"].find():
            print(doc)
    except Exception as e:
        print("Error consultando MongoDB:", e)


# ----------------------------
# Consultas NEO4J
# ----------------------------
if graph is not None:
    print("\nRelaciones en Neo4j:")
    try:
        query = """
        MATCH (c:Candidato)-[:POSTULO_A]->(o:Oferta)
        RETURN c.nombre, o.puesto
        """
        for record in graph.run(query):
            print(f"{record['c.nombre']} → {record['o.puesto']}")
    except Exception as e:
        print("Error consultando Neo4j:", e)


# ----------------------------
# Consultas REDIS
# ----------------------------
if r is not None:
    print("\nClaves en Redis:")
    try:
        # Listar todas las claves
        for key in r.scan_iter("*"):
            key_str = key.decode("utf-8")  # Convertir bytes a str
            tipo = r.type(key).decode("utf-8")  # Detectar tipo


            # Obtener valor según tipo
            if tipo == "string":
                value = r.get(key).decode("utf-8")
            elif tipo == "hash":
                value = {k.decode("utf-8"): v.decode("utf-8") for k, v in r.hgetall(key).items()}
            elif tipo == "list":
                value = [v.decode("utf-8") for v in r.lrange(key, 0, -1)]
            elif tipo == "set":
                value = [v.decode("utf-8") for v in r.smembers(key)]
            elif tipo == "zset":
                value = [(v.decode("utf-8"), s) for v, s in r.zrange(key, 0, -1, withscores=True)]
            else:
                value = f"<tipo {tipo}, no soportado para mostrar>"


            # Mostrar la clave y su valor
            print(f"{key_str} ({tipo}) → {value}")


    except Exception as e:
        print("Error consultando Redis:", e)
