from app.services.gemini.controller import process_user_prompt

async def ask_ai(prompt: str, context: str | None = None) -> str:
    """Interfaz pública para otros módulos."""
    return await process_user_prompt(prompt, context)
