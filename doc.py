import streamlit as st
from PyPDF2 import PdfReader
import textwrap
import pyttsx3
import tempfile

# ------------------------------
# Extract Text
# ------------------------------
def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text() or ""
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    else:
        st.error("Unsupported file type!")
    return text


# ------------------------------
# Split Text
# ------------------------------
def split_text(text, chunk_size=500):
    return textwrap.wrap(text, chunk_size)


# ------------------------------
# Offline TTS
# ------------------------------
def text_to_speech_offline(chunks, speed=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)

    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        engine.save_to_file(chunk, temp_file.name)
        temp_files.append(temp_file.name)

    engine.runAndWait()
    return temp_files


# ------------------------------
# UI
# ------------------------------
st.title("📄 Smart Document to Speech Converter (Offline)")

uploaded_file = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)

    if text.strip() == "":
        st.warning("No text found.")
    else:
        st.success("Text extracted!")

        chunk_size = st.slider("Chunk Size", 200, 1000, 500)
        speed = st.slider("Speech Speed", 100, 250, 150)

        chunks = split_text(text, chunk_size)

        st.info(f"Characters: {len(text)}")
        st.info(f"Chunks: {len(chunks)}")

        if st.button("Convert to Speech"):

            progress = st.progress(0)

            audio_files = text_to_speech_offline(chunks, speed)

            # Navigation
            if "index" not in st.session_state:
                st.session_state.index = 0

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Previous"):
                    st.session_state.index = max(0, st.session_state.index - 1)

            with col2:
                if st.button("Next"):
                    st.session_state.index = min(len(audio_files)-1, st.session_state.index + 1)

            # Play current chunk
            file = audio_files[st.session_state.index]
            with open(file, "rb") as f:
                st.audio(f.read(), format="audio/wav")

            progress.progress(1.0)