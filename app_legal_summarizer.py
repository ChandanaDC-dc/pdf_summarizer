import streamlit as st
import PyPDF2
from openai import OpenAI

# ==============================
# 🔑 CONFIGURATION
# ==============================
client = OpenAI(api_key=" ")

st.set_page_config(page_title="🌍 AI Legal Document Summarizer", layout="wide")

st.title("⚖️ AI-Powered Legal Document Summarizer (Multilingual)")
st.write("Upload a legal PDF document and get AI-generated summaries in multiple languages using OpenAI.")

# ==============================
# 📄 PDF TEXT EXTRACTION FUNCTION
# ==============================
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# ==============================
# 🧠 AI SUMMARIZATION FUNCTION
# ==============================
def summarize_text(text, style, language):
    if not text:
        return "No text found in the document."

    prompt = f"""
    You are a legal assistant AI.
    Read the following legal document and summarize it in **{style}** format.
    Then, translate the summary into **{language}**.
    Make sure the translation is natural and easy to understand.
    
    Document text:
    {text[:12000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI summarization and translation expert specialized in legal documents."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()

# ==============================
# 🌍 LANGUAGE OPTIONS
# ==============================
language_options = {
    "English": "English",
    "Kannada": "Kannada",
    "Hindi": "Hindi",
    "French": "French",
    "Telugu": "Telugu",
}

# ==============================
# 📤 FILE UPLOAD
# ==============================
uploaded_file = st.file_uploader("📎 Upload your legal PDF file", type=["pdf"])
selected_language = st.selectbox("🌐 Choose Output Language", list(language_options.keys()))

if uploaded_file:
    with st.spinner("📚 Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    if pdf_text:
        st.success("✅ Text extracted successfully!")
        st.subheader("📘 Original Extracted Text (Preview)")
        st.text_area("Preview", pdf_text[:2000] + "...", height=200)

        if st.button("🚀 Generate AI Summaries"):
            with st.spinner(f"🤖 Summarizing and translating into {selected_language}..."):
                bullet_summary = summarize_text(pdf_text, "bullet points", language_options[selected_language])
                paragraph_summary = summarize_text(pdf_text, "paragraph format", language_options[selected_language])

            st.subheader(f"🔹 Bullet Point Summary ({selected_language})")
            st.write(bullet_summary)

            st.subheader(f"🔸 Paragraph Summary ({selected_language})")
            st.write(paragraph_summary)

    else:
        st.warning("No text could be extracted from the PDF.")
else:
    st.info("Please upload a PDF file to get started.")

# ==============================
# 📘 FOOTER
# ==============================
st.markdown("---")
st.markdown("Developed by **Chandana DC** — powered by OpenAI GPT 🌐💡")
