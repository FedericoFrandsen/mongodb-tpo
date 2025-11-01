from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.skills import router as skills_router
from app.api.segment import router as segment_router
from app.api.recs import router as recs_router
from app.api.empresas import router as companies_router
from app.api.posiciones import router as positions_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(title="Talentum+ API")

app.include_router(users_router)
app.include_router(skills_router)
app.include_router(segment_router)
app.include_router(recs_router)
app.include_router(companies_router)
app.include_router(positions_router)
app.include_router(dashboard_router)