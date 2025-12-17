import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS

st.title("📘 Document-to-Speech Converter")
st.write("Upload a PDF or text file and I’ll read it for you!")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])

if uploaded_file:
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        text = uploaded_file.read().decode("utf-8")

    st.subheader("📝 Text Preview:")
    st.text_area("Extracted Text", text[:1000] + "..." if len(text) > 1000 else text, height=200)

    if st.button("🎧 Convert to Speech"):
        if text.strip():
            tts = gTTS(text)
            tts.save("speech.mp3")
            st.audio("speech.mp3")
            st.download_button("Download Speech", data=open("speech.mp3", "rb"), file_name="speech.mp3")
        else:
            st.error("No text found to read.")