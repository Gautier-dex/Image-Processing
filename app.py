import streamlit as st
import subprocess
import os
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="C-Image-Processor | Portfolio",
    page_icon="🎨",
    layout="wide"
)

# Compilation du moteur C (une seule fois au démarrage)
if not os.path.exists("./imageprocessing"):
    with st.spinner("Initialisation du moteur C..."):
        subprocess.run(["cmake", "."], capture_output=True)
        subprocess.run(["make"], capture_output=True)

# Style CSS pour l'esthétique
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True) # Correction de l'erreur ici

# Barre latérale (Sidebar)
with st.sidebar:
    st.title("⚙️ Configuration")
    filtre = st.selectbox("Choisir un filtre", [
        "Négatif", "Luminosité", "Binarisation (8bit)", 
        "Gris (24bit)", "Flou", "Flou Gaussien", "Netteté", "Contours", "Relief", "Égalisation"
    ])
    
    valeur = 0
    if filtre == "Luminosité":
        valeur = st.slider("Intensité", -100, 100, 30)
    elif filtre == "Binarisation (8bit)":
        valeur = st.slider("Seuil", 0, 255, 128)

    mapping = {
        "Négatif": 1, "Luminosité": 2, "Binarisation (8bit)": 3,
        "Gris (24bit)": 4, "Flou": 5, "Flou Gaussien": 6, "Netteté": 7, 
        "Contours": 8, "Relief": 9, "Égalisation": 55
    }

# Zone principale
st.title("🎨 Moteur de Traitement d'Image BMP")
uploaded_file = st.file_uploader("📥 Chargez une image BMP", type=['bmp'])

if uploaded_file:
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📷 Original")
        st.image("input.bmp", use_container_width=True)

    with col2:
        st.markdown("### 🚀 Résultat")
        if st.button("✨ Appliquer le traitement C"):
            cmd = ["./imageprocessing", "input.bmp", "output.bmp", str(mapping[filtre]), str(valeur)]
            subprocess.run(cmd, capture_output=True)
            
            if os.path.exists("output.bmp"):
                st.image("output.bmp", use_container_width=True)
                with open("output.bmp", "rb") as file:
                    st.download_button("📥 Télécharger", file, "resultat.bmp", "image/bmp")
            else:
                st.error("Erreur lors du traitement.")
