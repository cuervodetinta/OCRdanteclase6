import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import os

st.set_page_config(page_title="OCR con Audio", layout="centered")

# Estilo personalizado
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B3D2E;
        color: #B1FFCC;
    }
    h1 {
        color: white !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Reconocimiento óptico de Caracteres")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

if img_file_buffer is not None:
    # Leer imagen
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Aplicar filtro si se seleccionó
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # Mostrar imagen procesada
    st.image(img_rgb, caption="Imagen procesada", use_column_width=True)

    # OCR
    text = pytesseract.image_to_string(img_rgb)
    st.subheader("Texto detectado:")
    st.write(text)

    if text.strip() != "":
        # Convertir a audio
        tts = gTTS(text, lang='es')
        audio_path = "audio_temp.mp3"
        tts.save(audio_path)

        st.subheader("Reproducir audio:")
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Limpieza del archivo temporal
        audio_file.close()
        os.remove(audio_path)
    else:
        st.warning("No se detectó texto en la imagen.")


    


