from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI(
    title="FAQly AI",
    description="API para gestión de FAQs con embeddings y búsqueda inteligente",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status", tags=["System"])
async def get_status():
    return {
        "status": "success",
        "service": "FAQly AI API",
        "version": "0.1.0",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
