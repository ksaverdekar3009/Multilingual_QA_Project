````markdown
# 📚 Multilingual Document Q&A System

A simple full-stack application that lets users:

- Upload a **PDF document** (10–15 pages recommended)
- Ask questions in **multiple Indian languages** (English, Hindi, Gujarati, Marathi, Tamil, Bengali, Kannada, Telugu, etc.)
- Automatically:
  - Detect the **question language**
  - Translate the question ➜ **English**
  - Answer using **only the uploaded PDF content**
  - Translate the answer ➜ **back to the user’s language**

Frontend is built with **Streamlit**, and backend is built with **FastAPI**.

---

## 📂 Required Folder Structure

```text
/Multilingual_QA_Project
  /src              # all code (frontend + backend)
  /sample_pdfs      # 2 PDFs, 10–15 pages each
  /screenshots      # UI + sample Q&A screenshots
  README.md
````

Inside `/src`, the code is organized as:

```text
/src
  /backend
    main.py         # FastAPI app (API endpoints)
    qa_logic.py     # PDF handling, language detection, translation, QA logic

  /frontend
    app.py          # Streamlit UI

  /venv             # (optional) Python virtual environment
```

Place:

* Two sample PDFs in `/sample_pdfs`
* UI and Q&A screenshots in `/screenshots`

---

## 🧰 Dependencies

The project uses **Python 3.10+** and the following main libraries:

**Backend**

* `fastapi`
* `uvicorn[standard]`
* `python-multipart` (for file uploads via `UploadFile`)
* `PyPDF2` (PDF text extraction)
* `langdetect` (language detection)
* `deep-translator` (GoogleTranslator for translation)
* `transformers` (Hugging Face – QA model)
* `torch` (backend for the transformers model)

**Frontend**

* `streamlit`
* `requests` (to call FastAPI from Streamlit)

You can install all of these inside a virtual environment as shown below.

---

## 🔧 Installation (one-time setup)

1. **Go to the project root**

   ```bash
   cd Multilingual_QA_Project
   ```

2. **Create and activate a virtual environment**

   ```bash
   cd src
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   # source venv/bin/activate
   ```

3. **Install backend + frontend dependencies**

   ```bash
   pip install fastapi uvicorn[standard] python-multipart
   pip install PyPDF2 langdetect deep-translator transformers torch
   pip install streamlit requests
   ```

> ⚠️ If `torch` fails to install, use the command recommended on the official PyTorch website for your OS/CPU.

---

## ▶️ How to Run

You need **two terminals** (or two command prompts), both using the same virtual environment.

### 1️⃣ Start the Backend (FastAPI)

In **Terminal 1**:

```bash
cd Multilingual_QA_Project
cd src
venv\Scripts\activate        # if not already activated

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

* Backend runs at: `http://localhost:8000`
* API docs available at: `http://localhost:8000/docs`

Keep this terminal **open**.

---

### 2️⃣ Start the Frontend (Streamlit)

In **Terminal 2**:

```bash
cd Multilingual_QA_Project
cd src
venv\Scripts\activate        # same venv as backend

cd frontend
streamlit run app.py
```

* Frontend runs at: `http://localhost:8501`

Make sure the `BACKEND_URL` at the top of `frontend/app.py` matches the backend URL:

```python
BACKEND_URL = "http://localhost:8000"
```

---

## 💻 How to Use the App

1. **Open the Streamlit UI**
   Go to `http://localhost:8501` in your browser.

2. **📄 “Document” Tab**

   * Click **“⬆️ Upload & Extract Text”** and choose a PDF (10–15 pages).
   * Wait for extraction.
   * You’ll see:

     * File name
     * Justified preview of the first ~300 words
   * A hint explains that you should go to the **💬 Ask** tab to ask questions.

3. **💬 “Ask” Tab**

   * Type your question in any supported language.
   * Click **“🤔 Ask Question”**.
   * The system:

     * Detects the question language (e.g., `hi`, `gu`, `en`, etc.)
     * Translates question ➜ English
     * Answers from the uploaded PDF using a QA model
     * Translates answer ➜ back to the question language
   * The answer card shows:

     * Document name
     * Detected language code
     * Original question
     * Question translated to English
     * Answer in English
     * Answer translated to the original language

4. **🕒 “History” Tab**

   * Shows a list of previous questions and answers.
   * Each entry contains:

     * Original question + English version
     * Answer in English + translated answer
     * Document name and detected language code

---

## ⚠️ Notes & Limitations

* **In-memory storage**
  Uploaded PDF content is kept in a Python dictionary (`PDF_STORE`) while the backend is running.
  If you stop/restart the backend, you must re-upload PDFs.

* **Limited context**
  For simplicity, only the first ~3000 characters of the PDF text are used as context for the QA model due to input size limits.

* **Translation quality**
  Depends on `deep-translator`’s Google backend. Some languages may have better quality than others.

* **Initial load time**
  The first question can be slower because the QA model is loaded on the first call.

---

## 🔮 Future Improvements (Optional Ideas)

* Use a **retrieval-based** QA approach (chunking + embeddings + similarity search).
* Store documents and metadata in a **database** instead of memory.
* Add **user authentication** for multi-user deployments.
* Containerize with **Docker** and deploy backend + frontend to a cloud provider.

---

## 👤 Author

* **Name:** *Krishna Saverdekar*

```

If you want, I can also give you 2–3 bullet points to describe this in your project report or slide deck.
```
