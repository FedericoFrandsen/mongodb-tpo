from services.conexion_nosql import conectar_redis
from services.funciones import clear_offer_cache 
#Función que elimina cache de una oferta específica en Redis

ofertas = ["of-backend", "of-analista-datos", "of-especialista-ia"]

r = conectar_redis()
for ofid in ofertas:
    print(ofid, "->", clear_offer_cache(r, ofid))

#Llama a clear_offer_cache para borrar la cache asociada a esa oferta
#of-backend -> 5, los números representan cuántos elementos fueron eliminados del cache
