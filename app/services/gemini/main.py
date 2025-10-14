# app/services/gemini/main.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.gemini.schemas import AskRequest, AskResponse
from app.services.gemini.interface import ask_ai
from app.core.dependencies import get_current_user  # ← ya existente
from app.models.user import User  # o el modelo que uses

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_route(
    data: AskRequest,
    current_user: User = Depends(get_current_user)  # 🔒 protege el endpoint
):
    try:
        answer = await ask_ai(data.prompt, data.context)
        return AskResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
