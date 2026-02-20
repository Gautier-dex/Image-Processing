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
    /* Fond de la page */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Conteneur pour les images (Cartes blanches) */
    .image-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    /* Aligner le titre et le bouton */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
    }
    /* Enlever les espaces inutiles en haut */
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# [cite_start]Compilation du moteur C [cite: 134, 137, 140]
if not os.path.exists("./imageprocessing"):
    with st.spinner("🛠️ Initialisation du moteur C haute performance..."):
        [cite_start]subprocess.run(["cmake", "."], capture_output=True) [cite: 134, 140]
        [cite_start]subprocess.run(["make"], capture_output=True) [cite: 134, 141]

# Barre latérale (Sidebar) - Contrôles
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

    # [cite_start]Mapping vers ton main.c [cite: 22]
    mapping = {
        "Négatif": 1, "Luminosité": 2, "Binarisation (8bit)": 3,
        "Gris (24bit)": 4, "Flou": 5, "Flou Gaussien": 6, "Netteté": 7, 
        "Contours": 8, "Relief": 9, "Égalisation": 55
    }
    st.markdown("---")
    [cite_start]st.write("🔧 **Backend :** Exécutable C compilé via CMake") [cite: 1, 134]

# En-tête de la page principale
st.title("🎨 Moteur de Traitement d'Image BMP")
st.markdown("Cette application pilote un programme écrit en **C** pour manipuler les pixels et les headers d'images BMP.")

# Zone d'upload
uploaded_file = st.file_uploader("📥 Chargez une image BMP pour commencer", type=['bmp'])

if uploaded_file:
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Création des colonnes pour l'alignement côte à côte
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.subheader("📷 Image Originale")
        st.image("input.bmp", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.subheader("🚀 Résultat du Traitement")
        
        # [cite_start]Le bouton déclenche l'appel au code C [cite: 22, 141]
        if st.button("✨ Appliquer le traitement maintenant"):
            with st.spinner('Calculs en cours...'):
                [cite_start]cmd = ["./imageprocessing", "input.bmp", "output.bmp", str(mapping[filtre]), str(valeur)] [cite: 22, 31, 90]
                [cite_start]subprocess.run(cmd, capture_output=True) [cite: 31, 44]
                
                if os.path.exists("output.bmp"):
                    st.image("output.bmp", use_container_width=True)
                    with open("output.bmp", "rb") as file:
                        st.download_button("📥 Télécharger le résultat", file, "resultat.bmp", "image/bmp")
                else:
                    st.error("Erreur technique : l'image n'a pas pu être générée.")
        else:
            # Placeholder pour garder les colonnes alignées visuellement
            st.info("Sélectionnez un filtre à gauche et cliquez sur le bouton pour traiter.")
            # On ajoute un espace invisible pour simuler la hauteur de l'image originale
            st.markdown('<div style="height: 200px;"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Illustration du fonctionnement quand vide
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("1. Upload")
        st.write("Envoyez une image BMP 8 ou 24 bits.")
    with c2:
        st.subheader("2. Code C")
        st.write("Le moteur C traite la matrice de pixels.")
    with c3:
        st.subheader("3. Résultat")
        st.write("Visualisez et téléchargez l'image.")
