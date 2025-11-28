import json
import os
from sqlalchemy.orm import Session
import uuid
from app.api.v1.agent import repository
from app.api.v1.agent import schemas
from app.models.agent import Agent
from app.models.user import User
from app.models.knowledge_section import KnowledgeSection
from app.api.v1.agent.schemas import AgentListResponse
from app.services.gemini.interface import ask_ai
from pathlib import Path
from fastapi import HTTPException

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

def create_agent_service(db: Session, agent_data: schemas.AgentCreate, user_id: uuid.UUID):
    """
    Crea un nuevo agente con sus documentos y secciones relacionadas.
    Además, genera automáticamente la URL para el iframe.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError("El usuario especificado no existe.")

    new_agent = Agent(
        name=agent_data.name,
        instructions=agent_data.instructions,
        config=agent_data.config,
        created_by=user_id,
    )


    if agent_data.section_ids:
        sections = db.query(KnowledgeSection).filter(KnowledgeSection.knowledge_section_id.in_(agent_data.section_ids)).all()
        new_agent.sections.extend(sections)

    repository.save_agent(db, new_agent)

    return new_agent


def list_agents_service(db: Session, skip: int = 0, limit: int = 10, is_active: bool | None = None):
    total, agents = repository.get_agents(db, skip=skip, limit=limit, is_active=is_active)
    return AgentListResponse(total=total, agents=agents)

def get_agent_by_id(db: Session, agent_id: int):
        """
        Obtiene la información del agente por su ID.
        """
        return repository.get_agent_by_id(db, agent_id)

async def chat_with_agent(db: Session, agent_id: str, user_message: str) -> str | None:
    agent = repository.get_agent_by_id(db, agent_id)
    if not agent:
        return "No se encontró el agente especificado."

    sections = repository.get_agent_sections(db, agent_id)


    user_id = str(agent.created_by)
    base_upload_path = Path(UPLOAD_DIR) / str(user_id)

    context_parts = []
    for section in sections:
        documents = repository.get_documents_by_section(db, section.knowledge_section_id)
        for doc in documents:
            upload_path = os.path.join(base_upload_path, f"{doc.document_id}.json")
            print("📄 Revisando:", upload_path)

            if not os.path.exists(upload_path):
                print("⚠️ Archivo no encontrado:", upload_path)
                continue

            if not upload_path.endswith(".json"):
                print("➡️ Saltando archivo no JSON:", upload_path)
                continue

            try:
                with open(upload_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context_parts.append(json.dumps(data))
            except Exception as e:
                print(f"❌ Error leyendo {upload_path}: {e}")

    raw_context = "\n".join(context_parts)
    context = raw_context[:15000] if raw_context else None

    system_prompt = agent.instructions or "You are a helpful assistant."
    print("🧠 Contexto generado:", "Sí" if context else "No")

    if not context:
        return (
            "No se encontraron fuentes de datos asociadas al agente. "
            "Por favor, adjunta o vincula documentos en las secciones de conocimiento antes de continuar."
        )

    final_context = f"{system_prompt}\n\nContexto relevante:\n{context}"

    response = await ask_ai(name= agent.name,prompt=user_message, context=final_context)

    return response

def save_message_to_conversation(db: Session, conversation_id, user_message, bot_response):
    repository.save_message(
        db=db,
        conversation_id=conversation_id,
        user_message=user_message,
        bot_response=bot_response
    )
    
def create_conversation(db: Session, agent_id: str, title: str):
    # Validar que el agente pertenece al usuario
    agent = repository.get_agent_by_id(db, agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")


    conversation = repository.create(
        db=db,
        agent_id=agent_id,
        user_id=agent.created_by,
        title=title
    )

    return conversation