import fitz  # PyMuPDF
import docx
from uuid import UUID
import json
from datetime import datetime, timezone
from langdetect import detect
import os

def extract_text_from_pdf(file_path):
    """Extrae texto de un PDF, separado por páginas."""
    doc = fitz.open(file_path)
    text_chunks = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            text_chunks.append({
                "chunk_id": page_number,
                "text": text,
                "page": page_number,
                "embedding": None
            })
    doc.close()
    return text_chunks

def extract_text_from_docx(file_path):
    """Extrae texto de un archivo DOCX."""
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    paragraphs = text.split("\n\n")
    chunks = []
    for i, chunk in enumerate(paragraphs, start=1):
        chunks.append({
            "chunk_id": i,
            "text": chunk.strip(),
            "page": None,
            "embedding": None
        })
    return chunks

def detect_language_from_text(text):
    print("detectando lenguaje")
    """Detecta idioma del contenido."""
    try:
        return detect(text)
    except:
        return "unknown"

def generate_json_structure(file_path, uploaded_by , document_id):
    """Genera el JSON completo según el formato definido."""
    extension = file_path.split(".")[-1].lower()
    title = file_path.split("/")[-1]
    content_chunks = []

    if extension == "pdf":
        content_chunks = extract_text_from_pdf(file_path)
    elif extension in ["docx", "doc"]:
        content_chunks = extract_text_from_docx(file_path)
    elif extension in ["txt", "md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        content_chunks = [{"chunk_id": 1, "text": text, "page": None, "embedding": None}]
    else:
        raise ValueError("Formato de archivo no soportado")

    # Unir todo el texto para metadatos
    all_text = " ".join(chunk["text"] for chunk in content_chunks)
    language = detect_language_from_text(all_text[:1000])

    # Estructura JSON
    document_data = {
        "id": document_id,
        "title": title,
        "type": extension,
        "source": {
            "uploaded_by": uploaded_by,
            "uploaded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "original_filename": title
        },
        "metadata": {
            "pages": len(content_chunks),
            "language": language,
            "category": None,
            "tags": []
        },
        "content": {
            "summary": None,
            "chunks": content_chunks
        },
        "processing": {
            "status": "processed",
            "last_update": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "has_embeddings": False
        }
    }
    save_json_to_file(document_data, document_id ,uploaded_by)
    return document_data

def save_json_to_file(data, document_id, uploaded_by):
    def convert(o):
        """Convierte UUIDs, datetime y otros objetos no serializables a string."""
        if isinstance(o, UUID):
            return str(o)
        if hasattr(o, "isoformat"):  # datetime, date, etc.
            return o.isoformat()
        return str(o)

    user_folder = os.path.join("uploads", str(uploaded_by))
    os.makedirs(user_folder, exist_ok=True)

    output_path = os.path.join(user_folder, f"{document_id}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=convert)


