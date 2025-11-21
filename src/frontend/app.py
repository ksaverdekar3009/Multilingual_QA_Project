import requests
import streamlit as st
from typing import Dict, Any, List

# === CONFIG ===
BACKEND_URL = "http://localhost:8000"  # change this when you deploy backend


# === SESSION STATE SETUP ===
def init_session_state():
    if "pdf_id" not in st.session_state:
        st.session_state.pdf_id = None
    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = None
    if "preview" not in st.session_state:
        st.session_state.preview = None
    if "qa_history" not in st.session_state:
        # each item: {question, pdf_name, detected_lang, question_en, answer_en, answer_translated}
        st.session_state.qa_history: List[Dict[str, Any]] = []


# === BACKEND HELPERS ===
def upload_pdf_to_backend(uploaded_file) -> Dict[str, Any]:
    files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
    resp = requests.post(f"{BACKEND_URL}/upload_pdf", files=files, timeout=60)
    resp.raise_for_status()
    return resp.json()


def ask_backend(pdf_id: str, question: str) -> Dict[str, Any]:
    payload = {"pdf_id": pdf_id, "question": question}
    resp = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


# === UI HELPERS ===
def inject_css():
    st.markdown(
        """
        <style>
        /* Make background a bit softer */
        .main {
            background-color: #f5f7fb;
        }
        .page-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .page-subtitle {
            color: #6c757d;
            font-size: 0.95rem;
            margin-top: 0;
        }
        .card {
            padding: 1rem 1.25rem;
            border-radius: 0.9rem;
            border: 1px solid #e0e0e0;
            background-color: #ffffff;
            margin-bottom: 1rem;
        }
        .card-header {
            font-weight: 600;
            margin-bottom: 0.35rem;
        }
        .muted {
            color: #6c757d;
            font-size: 0.85rem;
        }
        .question-text {
            font-style: italic;
        }
        .answer-badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            font-size: 0.75rem;
            border-radius: 999px;
            background-color: #e9f5ff;
            color: #0d6efd;
            margin-bottom: 0.35rem;
        }
        .justified-text {
            text-align: justify;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div>
            <div class="page-title">📚 Multilingual Document Q&A</div>
            <p class="page-subtitle">
                Upload a PDF (10–15 pages) and ask questions in your own language.
                The system will detect the language, translate, and answer from the document.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚙️ App Settings")

        if st.session_state.pdf_id:
            st.success("📄 PDF is loaded and ready for Q&A.")
            st.write(f"**Current document:** {st.session_state.pdf_name}")
        else:
            st.info("No document uploaded yet.")

        st.markdown("---")
        st.markdown("### 🌐 Supported Languages")
        st.markdown(
            "- English (en)\n"
            "- Hindi (hi)\n"
            "- Gujarati (gu)\n"
            "- Marathi (mr)\n"
            "- Tamil (ta)\n"
            "- Bengali (bn)\n"
            "- Kannada (kn)\n"
            "- Telugu (te)"
        )


def render_upload_section():
    st.subheader("1️⃣ 📄 Upload & Process Document")

    upload_col, info_col = st.columns([1, 1.5], gap="large")

    with upload_col:
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if st.button("⬆️ Upload & Extract Text", use_container_width=True):
            if not uploaded_file:
                st.error("Please select a PDF file first.")
            else:
                with st.spinner("Uploading and reading the document..."):
                    try:
                        result = upload_pdf_to_backend(uploaded_file)
                        st.session_state.pdf_id = result["pdf_id"]
                        st.session_state.pdf_name = result["name"]
                        st.session_state.preview = result["preview"]
                        st.success("✅ PDF uploaded and processed successfully!")
                    except Exception as e:
                        st.error(f"Error uploading PDF: {e}")

    with info_col:
        st.markdown("#### 📝 Document Preview")
        if st.session_state.pdf_id:
            st.write(f"**File name:** {st.session_state.pdf_name}")
            st.write("**Extracted text (first ~300 words):**")

            preview = st.session_state.preview or ""
            if preview.strip():
                # JUSTIFIED PREVIEW TEXT
                st.markdown(
                    f"<div class='justified-text'>{preview}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.write("_No text extracted from this PDF._")

            # Instruction to move to Ask tab
            st.markdown(
                "<p class='muted'>💡 To ask questions about this document, switch to the "
                "<strong>💬 Ask</strong> tab at the top.</p>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Upload a document to see its preview here.")
            st.markdown(
                "<p class='muted'>After uploading, you can go to the <strong>💬 Ask</strong> tab "
                "to start asking questions about this document.</p>",
                unsafe_allow_html=True,
            )


def render_qa_section():
    st.subheader("2️⃣ 💬 Ask Questions")

    # Extra instructions with emojis
    st.markdown(
        "<p class='muted'>"
        "📝 <strong>Step 1:</strong> Type your question in any supported language.<br>"
        "🌐 <strong>Step 2:</strong> We detect the language and translate it to English.<br>"
        "🤖 <strong>Step 3:</strong> The answer is generated from the uploaded document and translated back."
        "</p>",
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "📝 Your question",
        placeholder="उदाहरण: इस दस्तावेज़ का मुख्य विषय क्या है? / What is this document about?",
        height=100,
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        ask_btn = st.button("🤔 Ask Question", type="primary", use_container_width=True)

    with col2:
        if st.session_state.pdf_id:
            st.markdown(
                "<p class='muted'>✅ Your question will be answered using the currently uploaded document.</p>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<p class='muted'>⚠️ Please upload a PDF in the <strong>📄 Document</strong> tab first.</p>",
                unsafe_allow_html=True,
            )

    if ask_btn:
        if not st.session_state.pdf_id:
            st.error("Please upload and process a PDF first.")
        elif not question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("🤖 Thinking based on your document..."):
                try:
                    result = ask_backend(st.session_state.pdf_id, question)
                except Exception as e:
                    st.error(f"Error contacting backend: {e}")
                    return

            # Save to history
            st.session_state.qa_history.append(
                {
                    "question": question,
                    "pdf_name": result["pdf_name"],
                    "detected_lang": result["detected_lang"],
                    "question_en": result["question_en"],
                    "answer_en": result["answer_en"],
                    "answer_translated": result["answer_translated"],
                }
            )

            render_answer_card(st.session_state.qa_history[-1])


def render_answer_card(item: Dict[str, Any]):
    st.markdown("### 🔍 Latest Answer")

    st.markdown(
        f"<div class='card-header'>💬 Answer from document: <strong>{item['pdf_name']}</strong></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p class='muted'>Detected language code: <code>{item['detected_lang']}</code></p>",
        unsafe_allow_html=True,
    )

    st.markdown("<p class='card-header'>❓ Your question</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='question-text'>{item['question']}</p>", unsafe_allow_html=True)

    st.markdown("<p class='card-header'>🌐 Question translated to English</p>", unsafe_allow_html=True)
    st.write(item["question_en"])

    st.markdown("<p class='card-header'>🧠 Answer (English)</p>", unsafe_allow_html=True)
    st.write(item["answer_en"])

    st.markdown(
        "<p class='card-header'>🌍 Answer (translated back to your language)</p>",
        unsafe_allow_html=True,
    )
    st.success(item["answer_translated"])

    st.markdown("</div>", unsafe_allow_html=True)


def render_history_section():
    if not st.session_state.qa_history:
        st.info("No questions asked yet.")
        return

    st.subheader("🕒 Question History")
    st.markdown("<p class='muted'>Newest questions appear first.</p>", unsafe_allow_html=True)

    # Show history reverse chronological
    for idx, item in enumerate(reversed(st.session_state.qa_history), start=1):
        with st.expander(f"Q{idx}: {item['question'][:60]}{'...' if len(item['question']) > 60 else ''}"):
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(
                f"<p class='muted'>📄 Document: <strong>{item['pdf_name']}</strong></p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='muted'>🌐 Detected language: <code>{item['detected_lang']}</code></p>",
                unsafe_allow_html=True,
            )
            st.markdown("**❓ Your question**")
            st.write(item["question"])

            st.markdown("**🌐 Question (English)**")
            st.write(item["question_en"])

            st.markdown("**🧠 Answer (English)**")
            st.write(item["answer_en"])

            st.markdown("**🌍 Answer (translated)**")
            st.write(item["answer_translated"])
            st.markdown("</div>", unsafe_allow_html=True)


# === MAIN APP ===
def main():
    st.set_page_config(
        page_title="Multilingual PDF Q&A",
        page_icon="📚",
        layout="wide",
    )
    inject_css()
    init_session_state()
    render_sidebar()
    render_header()

    # Tabs for clean navigation
    tab1, tab2, tab3 = st.tabs(["📄 Document", "💬 Ask", "🕒 History"])

    with tab1:
        render_upload_section()

    with tab2:
        render_qa_section()

    with tab3:
        render_history_section()


if __name__ == "__main__":
    main()
