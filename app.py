import streamlit as st
import subprocess
import os
from PIL import Image

st.set_page_config(
    page_title="BMP Studio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background-color: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
    color: #e8e6f0;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: #0f0f1a;
    border: 1.5px dashed #7c6af7;
    border-radius: 12px;
    padding: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #9080ff;
    box-shadow: 0 0 24px rgba(124,106,247,0.15);
}
[data-testid="stFileUploader"] label { color: #a0a0b8 !important; }
/* Browse files button — violet to match the theme, same position as default */
[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(135deg, #7c6af7 0%, #5a4fcf 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    box-shadow: 0 2px 12px rgba(124,106,247,0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    box-shadow: 0 4px 20px rgba(124,106,247,0.5) !important;
    background: linear-gradient(135deg, #9080ff 0%, #7c6af7 100%) !important;
}

[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e2e;
    transform: none !important;
    visibility: visible !important;
    display: block !important;
    min-width: 240px !important;
}
/* Custom sidebar toggle button — fixed top-left */
#sidebar-toggle {
    position: fixed;
    top: 14px;
    left: 14px;
    z-index: 99999;
    background: #16162a;
    border: 1px solid #2a2a40;
    border-radius: 7px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
#sidebar-toggle:hover {
    background: #1e1e38;
    border-color: #7c6af7;
    box-shadow: 0 0 16px rgba(124,106,247,0.25);
}
#sidebar-toggle svg {
    width: 16px;
    height: 16px;
    stroke: #7c6af7;
    stroke-width: 2;
    fill: none;
    stroke-linecap: round;
}
/* Bouton natif Streamlit — visible et stylisé, à sa position naturelle */
[data-testid="stSidebarCollapseButton"] button {
    background: #16162a !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 7px !important;
    color: #7c6af7 !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebarCollapseButton"] button:hover {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 16px rgba(124,106,247,0.3) !important;
}
[data-testid="stSidebarCollapseButton"] svg {
    stroke: #7c6af7 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #a0a0b8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #16162a !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 6px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div:focus-within {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.15) !important;
}
[data-testid="stSlider"] > div > div > div > div { background: #7c6af7 !important; }
[data-testid="stSlider"] > div > div > div { background: #2a2a40 !important; }


.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c6af7 0%, #5a4fcf 100%);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 14px 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    transition: all 0.2s ease;
    box-shadow: 0 4px 24px rgba(124,106,247,0.25);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(124,106,247,0.4);
}

[data-testid="stDownloadButton"] > button {
    width: 100%;
    background: transparent;
    color: #7c6af7;
    border: 1.5px solid #7c6af7;
    border-radius: 8px;
    padding: 10px 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    transition: all 0.2s ease;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(124,106,247,0.1);
}

[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #1e1e2e;
    display: block;
}

.stSpinner > div { border-top-color: #7c6af7 !important; }

/* Align both columns to the same top baseline */
[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
}

.bmp-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 6px;
}
.bmp-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: #5a5a78;
    letter-spacing: 0.04em;
    margin-bottom: 32px;
}
.bmp-accent { color: #7c6af7; }

.col-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    color: #a0a0c8;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.col-label::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #7c6af7;
    display: inline-block;
}

.sidebar-logo {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}
.sidebar-tag {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    color: #3a3a58;
    margin-bottom: 28px;
    letter-spacing: 0.06em;
}
.filter-badge {
    display: inline-block;
    background: rgba(124,106,247,0.12);
    color: #7c6af7;
    border: 1px solid rgba(124,106,247,0.25);
    border-radius: 4px;
    padding: 3px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    margin-top: 10px;
}
.divider { border: none; border-top: 1px solid #1e1e2e; margin: 20px 0; }

.stat-row { display: flex; gap: 10px; margin-top: 10px; }
.stat-box {
    flex: 1;
    background: #16162a;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #3a3a58;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}
.stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #e8e6f0;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── COMPILE ──
if not os.path.exists("./imageprocessing"):
    with st.spinner("Compilation du moteur C..."):
        subprocess.run(["cmake", "."], capture_output=True)
        subprocess.run(["make"], capture_output=True)


with st.sidebar:
    st.markdown('<div class="sidebar-logo">◈ BMP Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tag">Image Processing Engine · C Backend</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Space Mono, monospace; font-size:0.68rem; color:#3a3a58; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:10px;">Filtre</p>', unsafe_allow_html=True)
    filtre = st.selectbox("", [
        "Négatif", "Luminosité", "Binarisation (8bit)",
        "Gris (24bit)", "Flou", "Flou Gaussien", "Netteté", "Contours", "Relief", "Égalisation"
    ], label_visibility="collapsed")

    valeur = 0
    if filtre == "Luminosité":
        st.markdown('<p style="font-family: Space Mono, monospace; font-size:0.68rem; color:#3a3a58; letter-spacing:0.14em; text-transform:uppercase; margin: 16px 0 6px;">Intensité</p>', unsafe_allow_html=True)
        valeur = st.slider("", -100, 100, 30, label_visibility="collapsed")
    elif filtre == "Binarisation (8bit)":
        st.markdown('<p style="font-family: Space Mono, monospace; font-size:0.68rem; color:#3a3a58; letter-spacing:0.14em; text-transform:uppercase; margin: 16px 0 6px;">Seuil</p>', unsafe_allow_html=True)
        valeur = st.slider("", 0, 255, 128, label_visibility="collapsed")

    mapping = {
        "Négatif": 1, "Luminosité": 2, "Binarisation (8bit)": 3,
        "Gris (24bit)": 4, "Flou": 5, "Flou Gaussien": 6, "Netteté": 7,
        "Contours": 8, "Relief": 9, "Égalisation": 55
    }

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    filter_descriptions = {
        "Négatif": "Inverse chaque canal de couleur.",
        "Luminosité": "Ajuste l'exposition globale.",
        "Binarisation (8bit)": "Seuillage noir/blanc.",
        "Gris (24bit)": "Conversion en niveaux de gris.",
        "Flou": "Filtre box blur 3×3.",
        "Flou Gaussien": "Lissage gaussien doux.",
        "Netteté": "Accentue les bords et détails.",
        "Contours": "Détection de contours (Laplacien).",
        "Relief": "Effet de relief (emboss).",
        "Égalisation": "Égalisation d'histogramme."
    }
    st.markdown(f'<p style="font-family: DM Sans, sans-serif; font-size:0.82rem; color:#5a5a78; line-height:1.5;">{filter_descriptions[filtre]}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="filter-badge">CODE {mapping[filtre]:02d}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p style="font-family: Space Mono, monospace; font-size:0.65rem; color:#2a2a3a; letter-spacing:0.08em;">C · CMake · BMP8/24 · Convolution</p>', unsafe_allow_html=True)

# ── MAIN ──
st.markdown('<div class="bmp-title">Image Processing<span class="bmp-accent"> –</span> C</div>', unsafe_allow_html=True)
st.markdown('<div class="bmp-subtitle">Moteur de traitement BMP - 8 & 24 bits - pipeline C natif</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['bmp'], label_visibility="collapsed")

if not uploaded_file:
    st.markdown("""
    <div style="background:#0f0f1a; border:1.5px dashed #1e1e2e; border-radius:14px;
                padding:60px 40px; text-align:center; margin-top:10px;">
        <div style="font-size:2.5rem; margin-bottom:16px; opacity:0.3;">◈</div>
        <p style="font-family: Space Mono, monospace; font-size:0.78rem; color:#3a3a58;
                  letter-spacing:0.12em; text-transform:uppercase;">
            Chargez un fichier .bmp ci-dessus pour commencer
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    if os.path.exists("output.bmp"):
        os.remove("output.bmp")
    with open("input.bmp", "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        pil_img = Image.open("input.bmp")
        img_w, img_h = pil_img.size
        img_size_kb = round(os.path.getsize("input.bmp") / 1024, 1)
    except:
        img_w, img_h, img_size_kb = "—", "—", "—"

    # ── Button sits ABOVE the two columns so both images start at the same height ──
    apply = st.button(f"▶  Appliquer · {filtre.upper()}")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="col-label">Original</div>', unsafe_allow_html=True)
        st.image("input.bmp", use_container_width=True)
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-box">
                <div class="stat-label">Largeur</div>
                <div class="stat-value">{img_w}px</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Hauteur</div>
                <div class="stat-value">{img_h}px</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Taille</div>
                <div class="stat-value">{img_size_kb} KB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="col-label">Résultat — {filtre}</div>', unsafe_allow_html=True)

        if apply:
            with st.spinner(""):
                cmd = ["./imageprocessing", "input.bmp", "output.bmp",
                       str(mapping[filtre]), str(valeur)]
                result = subprocess.run(cmd, capture_output=True, text=True)

                if os.path.exists("output.bmp"):
                    st.image("output.bmp", use_container_width=True)
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                    with open("output.bmp", "rb") as f:
                        st.download_button(
                            "↓ Télécharger le résultat", f,
                            file_name=f"resultat_{filtre.lower().replace(' ', '_')}.bmp",
                            mime="image/bmp"
                        )
                else:
                    st.error("Erreur lors du traitement. Vérifiez le format de l'image.")
                    if result.stderr:
                        st.code(result.stderr, language="bash")
        else:
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center;
                        justify-content:center; min-height:300px; gap:12px;">
                <div style="font-size:2rem; opacity:0.08;">◈</div>
                <p style="font-family: Space Mono, monospace; font-size:0.7rem;
                           color:#2a2a40; letter-spacing:0.12em; text-transform:uppercase; margin:0;">
                    En attente du traitement
                </p>
            </div>
            """, unsafe_allow_html=True)
