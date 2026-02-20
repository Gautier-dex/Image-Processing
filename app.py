import streamlit as st
import subprocess
import os
from PIL import Image

# ── CONFIGURATION DE LA PAGE ──
st.set_page_config(
    page_title="BMP Studio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLE CSS (DESIGN & BOUTON SIDEBAR) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

.stApp {
    background-color: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
    color: #e8e6f0;
}

/* Cache les éléments inutiles */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── STYLISATION DU BOUTON BARRE LATÉRALE NATIF ── */
[data-testid="stSidebarCollapseButton"] button {
    background-color: #16162a !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 7px !important;
    color: #7c6af7 !important;
    position: fixed !important;
    top: 15px !important;
    left: 15px !important;
    z-index: 1000000 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebarCollapseButton"] button:hover {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 16px rgba(124,106,247,0.3) !important;
    background-color: #1e1e38 !important;
}

[data-testid="stSidebarCollapseButton"] svg {
    fill: #7c6af7 !important;
    stroke: #7c6af7 !important;
}

/* ── INTERFACE & CARTES ── */
[data-testid="stFileUploader"] {
    background: #0f0f1a;
    border: 1.5px dashed #7c6af7;
    border-radius: 12px;
    padding: 10px;
}

[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e2e;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c6af7 0%, #5a4fcf 100%);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 14px 20px;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    text-transform: uppercase;
    box-shadow: 0 4px 24px rgba(124,106,247,0.25);
}

.bmp-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    margin-left: 55px; /* Évite le chevauchement avec le bouton sidebar */
}

.bmp-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: #5a5a78;
    margin-left: 55px;
    margin-bottom: 32px;
}

.bmp-accent { color: #7c6af7; }

.col-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    color: #a0a0c8;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.stat-box {
    background: #16162a;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── COMPILATION DU MOTEUR C ──
if not os.path.exists("./imageprocessing"):
    with st.spinner("Compilation du moteur C..."):
        # Utilisation de CMake et Make pour générer l'exécutable [cite: 134, 140, 141]
        subprocess.run(["cmake", "."], capture_output=True)
        subprocess.run(["make"], capture_output=True)

# ── BARRE LATÉRALE ──
with st.sidebar:
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True) # Espace pour le bouton
    st.markdown('<p style="font-family: Space Mono, monospace; font-size:1.1rem; font-weight:700; color:white;">◈ BMP Studio</p>', unsafe_allow_html=True)
    st.markdown('---')
    
    filtre = st.selectbox("Sélectionner un filtre", [
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

# ── CORPS PRINCIPAL ──
st.markdown('<div class="bmp-title">Image Processing<span class="bmp-accent"> –</span> C</div>', unsafe_allow_html=True)
st.markdown('<div class="bmp-subtitle">Moteur de traitement BMP - Pipeline C natif</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['bmp'], label_visibility="collapsed")

if uploaded_file:
    # Sauvegarde de l'image d'entrée [cite: 44, 90]
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="col-label">Original</div>', unsafe_allow_html=True)
        st.image("input.bmp", use_container_width=True)

    with col2:
        st.markdown(f'<div class="col-label">Résultat — {filtre}</div>', unsafe_allow_html=True)
        
        if st.button("▶ APPLIQUER LE TRAITEMENT"):
            with st.spinner("Traitement en cours..."):
                # Exécution du programme C avec les arguments [cite: 44, 90]
                cmd = ["./imageprocessing", "input.bmp", "output.bmp", str(mapping[filtre]), str(valeur)]
                subprocess.run(cmd, capture_output=True)

                if os.path.exists("output.bmp"):
                    st.image("output.bmp", use_container_width=True)
                    with open("output.bmp", "rb") as f:
                        st.download_button("↓ Télécharger", f, file_name="resultat.bmp", mime="image/bmp")
                else:
                    st.error("Erreur technique lors du traitement.")
else:
    st.info("Veuillez charger une image BMP pour activer les commandes.")
