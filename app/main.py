from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import session
from app.api.v1 import api_router
from app.core.exceptions import init_exception_handlers
import datetime
from app.services.gemini.main import router as gemini_router

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://front-chatbot-demo.vercel.app",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicación...")
    session.Base.metadata.create_all(bind=session.engine)
    yield
    print("Cerrando aplicación...")

app = FastAPI(
    title="FAQly AI",
    description="API para gestión de FAQs con embeddings y búsqueda inteligente",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")
app.include_router(gemini_router, prefix="/api/v1/gemini", tags=["Gemini AI"])

@app.get("/status", tags=["System"])
async def get_status():
    return {
        "status": "success",
        "service": "FAQly AI API",
        "version": "0.1.0",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
