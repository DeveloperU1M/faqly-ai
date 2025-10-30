from app.services.gemini.controller import process_user_prompt

async def ask_ai(name: str, prompt: str, context: str | None = None) -> str:
    """Interfaz pública para otros módulos."""
    full_prompt = (
        f"CONTEXTO DE DATOS:\n---\n{context}\n---\n\n"
        f"PREGUNTA DEL USUARIO: {prompt}"
    )
    
    return await process_user_prompt(name, prompt, full_prompt)
