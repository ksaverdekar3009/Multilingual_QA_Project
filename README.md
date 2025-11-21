# Multilingual Document Q&A System

A simple full-stack application that lets users:

- Upload a PDF document (10–15 pages recommended)
- Ask questions in multiple Indian languages (English, Hindi, Gujarati, Marathi, Tamil, Bengali, Kannada and Telugu)
- Automatically:
  - Detect the question language
  - Translate the question ➜ English
  - Answer using only the uploaded PDF content
  - Translate the answer ➜ back to the user’s language

Frontend is built with Streamlit, and backend is built with FastAPI.

---

## Required Folder Structure
/Multilingual_QA_Project
  /src              # all code (frontend + backend)
  /sample_pdfs      # 2 PDFs, 10–15 pages each
  /screenshots      # UI + sample Q&A screenshots
  README.md

Inside /src, the code is organized as:
/src
  /backend
    main.py         # FastAPI app (API endpoints)
    qa_logic.py     # PDF handling, language detection, translation, QA logic

  /frontend
    app.py          # Streamlit UI

  /venv             # (optional) Python virtual environment


🧰 Dependencies
The project uses Python 3.10+ and the following main libraries:
Backend : fastapi,uvicorn[standard],python-multipart (for file uploads via UploadFile),PyPDF2 (PDF text extraction),langdetect (language detection),deep-translator (GoogleTranslator for translation),transformers (Hugging Face – QA model),torch (backend for the transformers model)

Frontend: streamlit,requests (to call FastAPI from Streamlit),

You can install all of these inside a virtual environment as shown below.

🔧 Installation (one-time setup)
Go to the project root : cd Multilingual_QA_Project

Create and activate a virtual environment : cd src
					    python -m venv venv
					    venv\Scripts\activate

Install backend + frontend dependencies : pip install fastapi uvicorn[standard] python-multipart
					  pip install PyPDF2 langdetect deep-translator transformers torch
					  pip install streamlit requests


▶️ How to Run
You need two terminals (or two command prompts), both using the same virtual environment.

1️ Start the Backend (FastAPI)
In Terminal 1:

cd Multilingual_QA_Project
cd src
venv\Scripts\activate        # if not already activated

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Backend runs at: http://localhost:8000
API docs available at: http://localhost:8000/docs
Keep this terminal open.

2️ Start the Frontend (Streamlit)
In Terminal 2:
cd Multilingual_QA_Project
cd src
venv\Scripts\activate        # same venv as backend

cd frontend
streamlit run app.py

Frontend runs at: http://localhost:8501

Make sure the BACKEND_URL at the top of frontend/app.py matches the backend URL:
BACKEND_URL = "http://localhost:8000"


⚠️ Notes & Limitations

In-memory storage
Uploaded PDF content is kept in a Python dictionary (PDF_STORE) while the backend is running.
If you stop/restart the backend, you must re-upload PDFs.

Limited context
For simplicity, only the first ~3000 characters of the PDF text are used as context for the QA model due to input size limits.

Translation quality
Depends on deep-translator’s Google backend. Some languages may have better quality than others.

Initial load time
The first question can be slower because the QA model is loaded on the first call.

👤 Author
Name: Krishna Saverdekar 
https://www.linkedin.com/in/krishna-saverdekar-aa709721b

Project: Multilingual Document Q&A System