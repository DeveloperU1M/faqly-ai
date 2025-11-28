from fastapi import APIRouter, Depends, HTTPException, Request, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.v1.agent import repository
from app.database.session import get_db
from app.api.v1.agent import service, schemas
from app.core.dependencies import get_current_user
from app.api.v1.agent.schemas import AgentListResponse
from uuid import UUID
from app.services.gemini.interface import ask_ai
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/", response_model=schemas.AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent_data: schemas.AgentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        new_agent = service.create_agent_service(db, agent_data, user_id=current_user.user_id)
        return new_agent
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=AgentListResponse)
def list_agents(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    is_active: bool | None = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    """
    📄 Lista todos los agentes registrados con soporte de paginación y filtros.
    """
    return service.list_agents_service(db=db, skip=skip, limit=limit, is_active=is_active)




@router.get("/{agent_id}", response_model=schemas.AgentResponse)
def get_agent_by_id(agent_id: UUID, db: Session = Depends(get_db)):
    agent = service.get_agent_by_id(db, agent_id)
    agent.welcome_message = f"¡Hola! Soy tu agente virtual {agent.name}. ¿Cómo puedo ayudarte hoy?"
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/{agent_id}/message/{conversation_id}", response_model=schemas.ChatResponse)
async def chat_with_agent( 
    agent_id: str,
    conversation_id: str,
    payload: schemas.ChatRequest,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    result = await service.chat_with_agent(db, agent_id, payload.message)

    if not result:
        raise HTTPException(status_code=500, detail="Error processing message")

    # Guardado en segundo plano
    background_tasks.add_task(
        service.save_message_to_conversation,
        db,
        conversation_id,
        payload.message,
        result
    )

    return schemas.ChatResponse(response=result)


@router.get("/embed/{agent_id}")
async def render_iframe(request: Request, agent_id: str, db: Session = Depends(get_db)):
    # 🔹 Obtener agente desde la base de datos
    agent = repository.get_agent_by_id(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agente no encontrado")

    # 🔹 Renderizar la plantilla HTML
    return templates.TemplateResponse(
        "embed.html",
        {
            "request": request,
            "agent": agent
        }
    )
    
@router.post("/conversations/create", response_model=schemas.ConversationResponse)
def create_conversation(
    body: schemas.ConversationCreate,
    db: Session = Depends(get_db)
):
    conversation = service.create_conversation(
        db=db,
        agent_id=body.agent_id,
        title=body.title
    )
    return conversation