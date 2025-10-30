from app.services.gemini.client import generate_content

async def process_user_prompt(name:str ,prompt: str, context: str | None = None):
    """Genera una respuesta basada en el prompt y contexto opcional."""
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    return await generate_content(name, full_prompt)
