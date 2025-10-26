from conexion_nosql import conectar_redis
from funciones import clear_offer_cache

ofertas = ["of-backend", "of-analista-datos", "of-especialista-ia"]

r = conectar_redis()
for ofid in ofertas:
    print(ofid, "->", clear_offer_cache(r, ofid))