# backend/qa_logic.py
import io
import uuid
from functools import lru_cache

from PyPDF2 import PdfReader
from langdetect import detect
from deep_translator import GoogleTranslator
from transformers import pipeline

# Simple in-memory storage: pdf_id -> {"name": str, "text": str, "preview": str}
PDF_STORE = {}


def extract_text_from_pdf(file_obj) -> str:
    """Read all pages from a PDF file-like object and return combined text."""
    reader = PdfReader(file_obj)
    all_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        all_text.append(text)
    return "\n".join(all_text)


def create_pdf_entry(uploaded_file) -> dict:
    """
    Takes an UploadFile (FastAPI) object, extracts text, stores it in memory,
    and returns metadata including pdf_id and a text preview.
    """
    # Read all bytes from the uploaded file
    pdf_bytes = uploaded_file.file.read()

    # Re-wrap bytes into a BytesIO for PyPDF2
    buf = io.BytesIO(pdf_bytes)

    text = extract_text_from_pdf(buf)
    words = text.split()
    preview_words = words[:300]
    preview = " ".join(preview_words)

    pdf_id = str(uuid.uuid4())
    PDF_STORE[pdf_id] = {
        "name": uploaded_file.filename,
        "text": text,
        "preview": preview,
    }

    return {
        "pdf_id": pdf_id,
        "name": uploaded_file.filename,
        "preview": preview,
    }


def detect_language(text: str) -> str:
    """Return ISO language code (e.g. 'en', 'hi', 'gu') or 'unknown'."""
    try:
        return detect(text)
    except Exception:
        return "unknown"


def translate_to_english(text: str, source_lang: str) -> str:
    """Translate text from source_lang to English."""
    if source_lang == "en":
        return text
    return GoogleTranslator(source=source_lang, target="en").translate(text)


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English text to target_lang."""
    if target_lang == "en":
        return text
    return GoogleTranslator(source="en", target=target_lang).translate(text)


@lru_cache(maxsize=1)
def get_qa_pipeline():
    """
    Load and cache the QA model so it only loads once.
    """
    return pipeline(
        "question-answering",
        model="distilbert-base-uncased-distilled-squad",
    )


def answer_question_from_pdf_text(question_en: str, pdf_text: str) -> str:
    """
    Very simple approach: take the first N characters of the PDF as context
    and ask the model to answer the question.
    """
    qa = get_qa_pipeline()
    max_chars = 3000
    context = pdf_text[:max_chars]

    if not context.strip():
        return "I could not find any readable text in the PDF."

    try:
        result = qa(question=question_en, context=context)
        return result.get("answer", "").strip()
    except Exception as e:
        return f"Error during QA: {e}"
