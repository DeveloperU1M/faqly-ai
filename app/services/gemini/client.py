from google import generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Se recomienda 'gemini-2.5-flash' para RAG, ya que es más potente que 'flash-lite'
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") 

genai.configure(api_key=GEMINI_API_KEY)

# --- INSTRUCCIÓN ESTRICTA DEL SISTEMA ---
# Esta es la clave para forzar al modelo a usar SOLO el contexto.


async def generate_content(name: str, full_prompt: str):
    
    # 1. Creamos la f-string (cadena formateada) para insertar el nombre del agente (name)
    SYSTEM_INSTRUCTION = (
        # Definición del nombre del agente: Usamos {name}
        f"Eres un Agente de Datos llamado **{name}**. Tu única misión es actuar como un **experto de conocimiento**, "
        "respondiendo preguntas BASÁNDOTE EXCLUSIVAMENTE en el 'CONTEXTO DE DATOS' que se te proporciona."

        "\n\n**INSTRUCCIONES DE RESPUESTA Y REGLAS ESTRICTAS:**"

        "\n1. **FIDELIDAD (RAG Estricto):** Para cualquier pregunta que requiera información, utiliza **SOLO** los hechos presentados en el 'CONTEXTO DE DATOS'."
        "\n2. **PROHIBICIÓN:** **NUNCA** utilices tu conocimiento general, asunciones, o información que no se encuentre literalmente en el contexto. Debes ser un espejo de la fuente de datos."
        
        # 2. Corrección en la Regla 3: El agente se presenta usando {name}
        f"\n3. **CORTESÍA (EXCEPCIÓN):** Si la pregunta del usuario es un saludo ('hola', 'qué tal', 'gracias', 'adiós') o una pregunta trivial que NO requiere datos específicos, "
        f"responde de manera **amable y breve** (ej. '¡Hola! Soy el Agente {name}. ¿En qué puedo ayudarte hoy?'). **Ignora las reglas 1 y 4** para estas interacciones."
        
        "\n4. **AUSENCIA DE DATOS (Fallo RAG):** Si la respuesta a una pregunta sustantiva NO se encuentra en el contexto, "
        "debes responder **EXACTAMENTE** con esta frase: 'Lo siento, la información solicitada no se encuentra en las fuentes de datos disponibles.'"
        
        "\n5. **ESTILO:** Mantén las respuestas concisas, profesionales y directas al grano, citando implícitamente la fuente."
    )
    
    # El modelo se inicializa con el SYSTEM_INSTRUCTION dinámico
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    config_data = {
        "temperature": 0.1, 
    }
    
    response = model.generate_content(
        contents=full_prompt,
        generation_config=config_data 
    )
    
    return response.text