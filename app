import streamlit as st
import subprocess
import os
from PIL import Image

st.set_page_config(page_title="C Image Processor", layout="wide")

st.title("🖼️ Traitement d'Image (C + Python)")
st.write("Cette application utilise un moteur de traitement d'image écrit en **C**.")

# Compilation automatique au lancement
if not os.path.exists("./imageprocessing"):
    with st.spinner("Compilation du moteur C en cours..."):
        subprocess.run(["cmake", "."])
        subprocess.run(["make"])

uploaded_file = st.file_uploader("Choisissez une image BMP (8-bit recommandé)", type=['bmp'])

if uploaded_file:
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    col_ctrl, col_res = st.columns([1, 2])

    with col_ctrl:
        option = st.selectbox("Filtre à appliquer :", ["negative", "threshold", "brightness", "outline"])
        btn = st.button("Lancer le traitement")

    if btn:
        # Appel de l'exécutable généré par ton CMake
        result = subprocess.run(["./imageprocessing", "input.bmp", "output.bmp", option], capture_output=True)
        
        if result.returncode == 0:
            c1, c2 = st.columns(2)
            with c1:
                st.image("input.bmp", caption="Original", use_container_width=True)
            with c2:
                st.image("output.bmp", caption=f"Résultat : {option}", use_container_width=True)
        else:
            st.error("Erreur lors du traitement par le programme C.")
