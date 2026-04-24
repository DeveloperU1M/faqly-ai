# Faqly AI (DocuChat) 🤖📄

Faqly AI es una plataforma **SaaS de vanguardia** diseñada para transformar documentos estáticos en asistentes conversacionales inteligentes. Utilizando técnicas de **RAG (Retrieval-Augmented Generation)**, el sistema permite a los usuarios interactuar con sus archivos (`.pdf`, `.docx`, `.pptx`) de manera natural, obteniendo respuestas precisas basadas exclusivamente en el contexto proporcionado.

---

## 🚀 Características Principales

- **Procesamiento Multiformato:** Extracción de texto y segmentación inteligente de archivos PDF, Word y PowerPoint.
- **Motor RAG Avanzado:** Generación de embeddings y almacenamiento en base de datos vectorial para búsquedas semánticas de alta velocidad.
- **Integración con Gemini:** Aprovecha los modelos de lenguaje de última generación de Google para respuestas coherentes y contextualizadas.
- **Arquitectura Escalable:** Construido con un enfoque de alto rendimiento para el manejo de múltiples usuarios y documentos.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.12+ |
| Framework API | FastAPI (Asíncrono y de alto rendimiento) |
| LLM & IA | Google Gemini API |
| Procesamiento de Documentos | LangChain / PyMuPDF |
| Infraestructura | Docker & Docker Compose |
| Servidor Web | Nginx (como Proxy Inverso) |

---

## 📦 Instalación y Configuración

### Requisitos Previos

- Docker y Docker Compose
- API Key de Google Gemini

### Pasos para el despliegue

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/faqly-ai.git
   cd faqly-ai
   ```

2. **Configurar variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto:

   ```env
   GEMINI_API_KEY=tu_api_key_aqui
   DATABASE_URL=postgresql://user:password@db:5432/faqly_db
   DEBUG=True
   ```

3. **Levantar con Docker:**

   ```bash
   docker-compose up --build
   ```

   La API estará disponible en `http://localhost:8000` y la documentación interactiva en `/docs`.

---

## 🏗️ Arquitectura del Sistema

El flujo de datos sigue este proceso:

```
Usuario
   |
   | (1) Sube documento
   v
FastAPI Endpoint
   |
   | (2) Chunking — división en fragmentos manejables
   v
Motor de Vectorización
   |
   | (3) Embeddings almacenados en base de datos vectorial
   v
Base de Datos Vectorial
   |
   | (4) Recuperación de fragmentos relevantes (RAG)
   v
Google Gemini API
   |
   | (5) Respuesta contextualizada
   v
Usuario
```

| Paso | Descripción |
|---|---|
| **Ingesta** | El usuario sube un documento mediante un endpoint de FastAPI |
| **Chunking** | El sistema divide el texto en fragmentos manejables |
| **Vectorización** | Se generan vectores de los fragmentos y se almacenan |
| **Consulta** | Se recuperan los fragmentos más relevantes y se envían a Gemini para generar la respuesta final |

---

## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).
