import streamlit as st
import subprocess
import os
from PIL import Image

st.set_page_config(page_title="C Image Processor Pro", layout="wide")

st.title("🖼️ Traitement d'Image BMP (Moteur C)")
st.write("Déployé par Gautier - Moteur de traitement haute performance en C")

# Compilation automatique
if not os.path.exists("./imageprocessing"):
    subprocess.run(["cmake", "."])
    subprocess.run(["make"])

uploaded_file = st.file_uploader("Chargez une image BMP", type=['bmp'])

if uploaded_file:
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.sidebar:
        st.header("Paramètres")
        filtre = st.selectbox("Action", [
            "Négatif", "Luminosité", "Binarisation (8bit)", 
            "Gris (24bit)", "Flou", "Netteté", "Contours", "Égalisation"
        ])
        
        valeur = 0
        if filtre == "Luminosité":
            valeur = st.slider("Intensité", -100, 100, 20)
        if filtre == "Binarisation (8bit)":
            valeur = st.slider("Seuil", 0, 255, 128)

        # Mapping vers les numéros de ton main.c
        mapping = {
            "Négatif": 1, "Luminosité": 2, "Binarisation (8bit)": 3,
            "Gris (24bit)": 4, "Flou": 5, "Netteté": 7, 
            "Contours": 8, "Égalisation": 55
        }

    if st.button("Lancer le traitement C"):
        cmd = ["./imageprocessing", "input.bmp", "output.bmp", str(mapping[filtre]), str(valeur)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists("output.bmp"):
            col1, col2 = st.columns(2)
            with col1:
                st.image("input.bmp", caption="Original")
            with col2:
                st.image("output.bmp", caption=f"Résultat {filtre}")
        else:
            st.error("Erreur technique dans le moteur C.")
            st.code(result.stderr)
