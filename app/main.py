from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.skills import router as skills_router
from app.api.segment import router as segment_router
from app.api.recs import router as recs_router
from app.api.empresas import router as empresas_router
from app.api.posiciones import router as posiciones_router
from app.api.dashboard import router as dashboard_router
from app.api.cursos import router as cursos_router
from app.api.inscripciones import router as inscripciones_router

app = FastAPI(title="Talentum+ API")

app.include_router(users_router)        # /users
app.include_router(skills_router)       # /skills
app.include_router(segment_router)      # /segment
app.include_router(recs_router)         # /offers/...
app.include_router(empresas_router)     # /empresas
app.include_router(posiciones_router)   # /posiciones
app.include_router(dashboard_router)    # /dashboard
app.include_router(cursos_router)       # /cursos
app.include_router(inscripciones_router) # /inscripciones