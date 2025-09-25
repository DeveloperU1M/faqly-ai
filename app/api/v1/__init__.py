# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1.users.routes import router as users_router
from app.api.v1.knowledge_sections.routes import router as knowledge_sections

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(knowledge_sections)

