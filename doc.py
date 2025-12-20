import streamlit as st
from gtts import gTTS
import io
from PyPDF2 import PdfReader

# ------------------------------
# Helper function to extract text
# ------------------------------
def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text()
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    else:
        st.error("Unsupported file type!")
    return text

# ------------------------------
# Streamlit Interface
# ------------------------------
st.title("📄 Document to Speech Converter")

uploaded_file = st.file_uploader("Upload a TXT or PDF file", type=["txt", "pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)

    if text.strip() == "":
        st.warning("The uploaded document is empty or could not extract text.")
    else:
        if st.button("Convert to Speech"):
            try:
                tts = gTTS(text)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)  # write audio to memory
                mp3_fp.seek(0)
                st.audio(mp3_fp, format="audio/mp3")
            except Exception as e:
                st.error(f"Error during text-to-speech conversion: {e}")
