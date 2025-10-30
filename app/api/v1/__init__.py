# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1.users.routes import router as users_router
from app.api.v1.knowledge_sections.routes import router as knowledge_sections
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.documents.routes import router as documents_router
from app.api.v1.agent.routes import router as agent_router
api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(knowledge_sections)
api_router.include_router(auth_router)
api_router.include_router(documents_router)
api_router.include_router(agent_router)


