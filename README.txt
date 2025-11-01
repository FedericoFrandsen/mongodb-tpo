# mongodb-tpo

# Talentum+ API

API de demostración para matching de candidatos y ofertas usando:
- MongoDB (fuente de verdad de candidatos y ofertas)
- Neo4j (relaciones: postulaciones, etc.)
- Redis (cache de recomendaciones y sets por skill)
- FastAPI (endpoints)

## Arquitectura (visión rápida)

- MongoDB
  - Colecciones: `candidatos`, `ofertas`, `empresas`, …
  - Los candidatos se guardan con:
    - `informacion_personal.nombre_apellido`, `email`
    - `estado`, `habilidades.tecnicas` (lista de `{nombre, nivel}`)
    - `fecha_creacion` (Date)
  - Las ofertas se guardan con:
    - `puesto`, `requerimientos` (lista de `{habilidad, nivel}`), `estado`, `fecha_creacion`

- Neo4j
  - Modelo grafo para postulaciones:
    - `(Candidato)-[:POSTULA_A|:POSTULO_A]->(Oferta {id})`
  - Nodos extra (Empresa, Curso, etc.) para enriquecer el caso de uso (opcional).

- Redis
  - Cache de recomendaciones: `cache:match:{oferta_id}` (ZSET con score por candidato)
  - Índices por skill: `skill:{skill}:users` (SET de usuarios)
  - Cache de perfil (opcional): `user:{nombre}` con TTL.

- FastAPI
  - Users (alta y actualización de skills)
  - Segment (intersección por skills con Redis)
  - Recommendations (recompute + read + invalidate)

## Endpoints

### Users

#### POST /users
Crea un candidato en Mongo y actualiza índices Redis.

Body (ejemplo):
```json
{
  "nombre": "camila gebara",
  "email": "camila@example.com",
  "skills": ["python", "tensorflow", "machine learning"]
}
```

Efectos:
- Mongo: inserta documento en `candidatos` con estado=activo, fecha_creacion (Date) y skills (nivel=5 por defecto).
- Redis:
  - `skill:{skill}:users` → agrega el usuario a cada set de skill.
  - `user:{nombre}` → cachea perfil (TTL).

---

### Skills

#### POST /skills/add
Agrega un skill a un candidato y actualiza los sets Redis.

Body:
```json
{
  "user": "camila gebara",
  "skill": "fastapi"
}
```

Efectos:
- Mongo: `candidatos.update_one` con `$addToSet`.
- Redis:
  - `skill:fastapi:users` → agrega “camila gebara”
  - Invalida `user:{camila gebara}` si existe.

---

### Segment

#### GET /segment?skills=python&skills=fastapi
Segmenta usuarios por intersección de skills.

- Lee en Redis la intersección de sets `skill:{s}:users`.
- Enriquecer desde Mongo perfiles de esos usuarios.

Responde:
```json
{
  "skills": ["python", "fastapi"],
  "users": ["camila gebara"],
  "perfiles": [...]
}
```

---

### Recommendations (por oferta)

El `oferta_id` es un ID simbólico. Se mapea internamente a un “puesto” en `funciones.py`:

```python
# funciones.py
def _puesto_por_oferta_id(oferta_id: str) -> str:
    return {
        "of-backend": "Desarrollador Backend",
        "of-analista-datos": "Analista de Datos",
        "of-especialista-ia": "Especialista en IA",
    }.get(oferta_id, "")
```

Con ese “puesto”, se busca en Mongo la oferta (colección `ofertas`) para obtener los requerimientos.

#### GET /offers/{oferta_id}/recommendations
Obtiene recomendaciones (cache-first).

- Si `cache:match:{oferta_id}` existe en Redis:
  - Devuelve `source: "redis"`
- Si no existe:
  - Toma lock (SET NX) y ejecuta recompute → `source: "recomputed"`
  - Si otro proceso está recomputando, espera 2s → `source: "delayed-redis"`

Responde:
```json
{
  "source": "redis | recomputed | delayed-redis",
  "recs": [["camila gebara", 51.0], ...],
  "perfiles": [ ... ]
}
```

#### POST /offers/{oferta_id}/recompute
Fuerza el recálculo ahora.

- Busca la oferta en Mongo por el “puesto” mapeado.
- Trae postulados a esa oferta desde Neo4j.
- Calcula score y escribe ZSET `cache:match:{oferta_id}` con TTL.

#### DELETE /offers/{oferta_id}/cache
Invalida la cache de recomendaciones para una oferta.

---