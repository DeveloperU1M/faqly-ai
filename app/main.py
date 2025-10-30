from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import session
from app.api.v1 import api_router
from app.core.exceptions import init_exception_handlers
import datetime
from app.services.gemini.main import router as gemini_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Iniciando aplicación...")
    session.Base.metadata.create_all(bind=session.engine)
    yield
    # Shutdown
    print("Cerrando aplicación...")

app = FastAPI(
    title="FAQly AI",
    root_path="/faqly-ai",
    description="API para gestión de FAQs con embeddings y búsqueda inteligente",
    version="0.1.0",
    lifespan=lifespan
)

init_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://front-chatbot-demo-a73e.vercel.app",
        "https://www.front-chatbot-demo-a73e.vercel.app",
        "http://127.0.0.1:64809"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
@app.get("/status", tags=["System"])
async def get_status():
    return {
        "status": "success",
        "service": "FAQly AI API",
        "version": "0.1.0",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

app.include_router(gemini_router, prefix="/api/v1/gemini", tags=["Gemini AI"])