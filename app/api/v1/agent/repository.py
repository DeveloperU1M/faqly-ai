from sqlalchemy.orm import Session
from app.models.agent import Agent
from app.models.document import Document
from app.models.knowledge_section import KnowledgeSection


def save_agent(db: Session, agent: Agent):
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


def get_agent_by_id(db: Session, agent_id):
    return db.query(Agent).filter(Agent.agent_id == agent_id).first()

def get_agents(db: Session, skip: int = 0, limit: int = 10, is_active: bool | None = None):
    query = db.query(Agent)
    
    if is_active is not None:
        query = query.filter(Agent.is_active == is_active)

    total = query.count()
    agents = query.order_by(Agent.created_at.desc()).offset(skip).limit(limit).all()

    return total, agents

def get_agent_by_id(db: Session, agent_id: int):
    """
    Consulta en la base de datos el agente según su ID.
    """
    return db.query(Agent).filter(Agent.agent_id == agent_id).first()

def get_agent_by_id(db: Session, agent_id: str):
    """
    Obtiene los datos básicos del agente.
    """
    return (
        db.query(Agent)
        .filter(Agent.agent_id == agent_id, Agent.is_active == True)
        .first()
    )


def get_agent_sections(db: Session, agent_id: str):
    """
    Obtiene las secciones asociadas al agente.
    """
    # Aquí hacemos join con la tabla intermedia agent_sections
    return (
        db.query(KnowledgeSection)
        .join(Agent.sections)  # join automático por la relación many-to-many
        .filter(Agent.agent_id == agent_id, Agent.is_active == True)
        .all()
    )
def get_documents_by_section(db: Session, section_id: str):
    return (
        db.query(Document)
        .filter(Document.section_id == section_id)
        .all()
    )