from services.conexion_nosql import conectar_redis
from services.funciones import clear_offer_cache

ofertas = ["of-backend", "of-analista-datos", "of-especialista-ia"]

r = conectar_redis()
for ofid in ofertas:
    print(ofid, "->", clear_offer_cache(r, ofid))