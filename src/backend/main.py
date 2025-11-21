# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from qa_logic import (
    create_pdf_entry,
    PDF_STORE,
    detect_language,
    translate_to_english,
    translate_from_english,
    answer_question_from_pdf_text,
)

app = FastAPI(title="Multilingual PDF Q&A Backend")

# Allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    pdf_id: str
    question: str


class AskResponse(BaseModel):
    pdf_name: str
    detected_lang: str
    question_en: str
    answer_en: str
    answer_translated: str
    preview: str


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    result = create_pdf_entry(file)
    return result


@app.post("/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    pdf_entry = PDF_STORE.get(req.pdf_id)
    if not pdf_entry:
        raise HTTPException(status_code=404, detail="PDF not found")

    pdf_text = pdf_entry["text"]
    pdf_name = pdf_entry["name"]
    preview = pdf_entry["preview"]

    detected_lang = detect_language(req.question)
    question_en = translate_to_english(req.question, detected_lang)
    answer_en = answer_question_from_pdf_text(question_en, pdf_text)
    answer_translated = translate_from_english(answer_en, detected_lang)

    return AskResponse(
        pdf_name=pdf_name,
        detected_lang=detected_lang,
        question_en=question_en,
        answer_en=answer_en,
        answer_translated=answer_translated,
        preview=preview,
    )
