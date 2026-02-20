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

# Style CSS pour habiller la page et aligner les éléments
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .image-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
        min-height: 400px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Compilation du moteur C (uniquement si l'exécutable n'existe pas)
if not os.path.exists("./imageprocessing"):
    subprocess.run(["cmake", "."], capture_output=True)
    subprocess.run(["make"], capture_output=True)

# Barre latérale (Sidebar)
with st.sidebar:
    st.title("⚙️ Réglages")
    st.markdown("---")
    filtre = st.selectbox("🎯 Choisir un filtre", [
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
    st.markdown("---")
    st.write("🔧 **Backend :** Exécutable C compilé via CMake")

# Corps principal
st.title("🎨 Moteur de Traitement d'Image BMP")
uploaded_file = st.file_uploader("📤 Chargez une image BMP", type=['bmp'])

if uploaded_file:
    # Nettoyage d'un ancien résultat pour éviter les faux positifs
    if os.path.exists("output.bmp"):
        os.remove("output.bmp")
        
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.subheader("📷 Image Originale")
        st.image("input.bmp", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.subheader("🚀 Résultat")
        
        # Le bouton d'action
        process_btn = st.button("✨ Appliquer le traitement")
        
        if process_btn:
            with st.spinner('Traitement C en cours...'):
                cmd = ["./imageprocessing", "input.bmp", "output.bmp", str(mapping[filtre]), str(valeur)]
                subprocess.run(cmd, capture_output=True)
                
                if os.path.exists("output.bmp"):
                    st.image("output.bmp", use_container_width=True)
                    with open("output.bmp", "rb") as file:
                        st.download_button("📥 Télécharger", file, "resultat.bmp", "image/bmp")
                else:
                    st.error("Erreur lors de la génération de l'image.")
        else:
            st.info("Sélectionnez vos réglages à gauche et validez ici.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Veuillez uploader une image pour activer l'interface de comparaison.")
