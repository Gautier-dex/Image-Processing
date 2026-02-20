import streamlit as st
import subprocess
import os
from PIL import Image

# Configuration de la page avec un titre et une icône
st.set_page_config(
    page_title="C-Image-Processor | Portfolio",
    page_icon="🎨",
    layout="wide"
)

# Style CSS personnalisé pour améliorer l'apparence
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stSelectbox, .stSlider {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_stdio=True)

# Barre latérale (Sidebar) pour les contrôles
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/18/C_Programming_Language.svg", width=100)
    st.title("Configuration")
    st.info("Ce projet démontre l'intégration de code C performant dans une interface moderne.")
    
    filtre = st.selectbox("🎯 Choisir un filtre", [
        "Négatif", "Luminosité", "Binarisation (8bit)", 
        "Gris (24bit)", "Flou", "Flou Gaussien", "Netteté", "Contours", "Relief", "Égalisation"
    ])
    
    valeur = 0
    if filtre == "Luminosité":
        valeur = st.slider("Intensité de la lumière", -100, 100, 30)
    elif filtre == "Binarisation (8bit)":
        valeur = st.slider("Seuil de binarisation", 0, 255, 128)

    # [cite_start]Mapping précis vers ton main.c [cite: 1]
    mapping = {
        "Négatif": 1, "Luminosité": 2, "Binarisation (8bit)": 3,
        "Gris (24bit)": 4, "Flou": 5, "Flou Gaussien": 6, "Netteté": 7, 
        "Contours": 8, "Relief": 9, "Égalisation": 55
    }
    
    st.divider()
    st.markdown("### 🛠️ Backend")
    st.code("Langage : C11\nLib : Standard + Math")

# Zone principale
st.title("🎨 Moteur de Traitement d'Image BMP")
st.subheader("Algorithmes de convolution et manipulation de headers en C")

uploaded_file = st.file_uploader("📤 Chargez votre image BMP pour tester", type=['bmp'])

if uploaded_file:
    # Sauvegarde temporaire
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📷 Avant")
        st.image("input.bmp", use_container_width=True)

    with col2:
        st.markdown("### 🚀 Après")
        if st.button("✨ Appliquer le traitement"):
            with st.spinner('Le moteur C traite l\'image...'):
                # [cite_start]Commande vers ton exécutable compilé [cite: 1]
                cmd = ["./imageprocessing", "input.bmp", "output.bmp", str(mapping[filtre]), str(valeur)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if os.path.exists("output.bmp"):
                    st.image("output.bmp", use_container_width=True)
                    # Option de téléchargement
                    with open("output.bmp", "rb") as file:
                        st.download_button(
                            label="📥 Télécharger le résultat",
                            data=file,
                            file_name=f"resultat_{filtre}.bmp",
                            mime="image/bmp"
                        )
                else:
                    st.error("Une erreur est survenue lors du traitement.")
                    st.code(result.stderr)
        else:
            st.info("Cliquez sur le bouton ci-dessus pour voir le résultat.")

else:
    # Message d'accueil quand aucune image n'est chargée
    st.write("---")
    st.warning("Veuillez charger une image BMP pour activer les filtres.")
    st.markdown("""
    ### Pourquoi ce projet ?
    - [cite_start]**Performance** : Traitement de bas niveau en C sans bibliothèques externes lourdes[cite: 1].
    - [cite_start]**Maîtrise** : Gestion manuelle des structures BMP et de la mémoire[cite: 1].
    - **Polyvalence** : Intégration C/Python pour un rendu utilisateur fluide.
    """)
