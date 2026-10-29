"""UI de Streamlit del sistema experto de cultivos (AMBA).

Único archivo con lógica de presentación. No contiene texto propio del
dominio: todas las frases salen de textos.py (plantillas C.6 y C.7).

Principios de diseño aplicados:
  - Jerarquía visual: hero grande, secciones con icon Material, cards con
    header + chips + contenido.
  - Color para codificar significado: verde=recomendado, ámbar=advertencia,
    gris=descartado por época, azul=info estacional.
  - Tipografía Inter (Google Fonts) sobre el theme oscuro del config.toml.
  - Densidad controlada: 2 columnas para recomendados, 3 para pautas,
    chips compactos para estado.
"""
from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

import facts  # noqa: F401  (aplica el parche de collections.Mapping)
from assets import (
    EMPTY_STATE_SVG,
    HERO_SCENE_SVG,
    LOGO_SVG,
    PERFIL_ICON_ESPACIO,
    PERFIL_ICON_MES,
    PERFIL_ICON_PROFUNDIDAD,
    PERFIL_ICON_RIEGO,
    PERFIL_ICON_SOL,
    icono_cultivo,
)
from loader import cargar_cultivos
from knowledge_base import ejecutar_motor
from textos import (
    AVISO_FIJO,
    FRASE_RIEGO,
    MESES_NOMBRE,
    MOTIVOS_DESCARTE,
    OPCIONES_CUIDADO,
    TEMAS_PAUTA,
    etiqueta_luz,
    render,
    render_cumple_o_falla,
    render_descarte_epoca,
)


# ============================================================
# Config
# ============================================================

RUTA_CSV = Path(__file__).parent / "data" / "cultivos_v6.csv"

# Favicon: reusamos nuestro LOGO_SVG como data URI así la pestaña del
# browser muestra el brote verde con gradiente, en lugar del icono negro
# monocromo que trae Material por default.
_FAVICON = f"data:image/svg+xml;base64,{base64.b64encode(LOGO_SVG.encode('utf-8')).decode('ascii')}"

st.set_page_config(
    page_title="Selector de cultivos",
    page_icon=_FAVICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS global
# ============================================================

CSS = """
<style>
    /* ---------- Tipografía ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, .stApp, .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* ---------- Layout ---------- */
    .main .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1240px;
    }
    hr { border-color: #243530 !important; margin: 2rem 0 !important; }

    /* ---------- Hero ---------- */
    .hero {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        padding: 0 0 1rem;
    }
    .hero-mark {
        flex-shrink: 0;
        align-self: flex-start;
        margin-top: 0.35rem;
        filter: drop-shadow(0 0 24px rgba(74, 222, 128, 0.25));
    }
    .hero-mark svg { width: 68px; height: 68px; display: block; }
    .hero-text { flex: 1; min-width: 0; }
    .hero-scene {
        flex-shrink: 0;
        align-self: flex-start;
        margin-top: 0.35rem;
        width: 340px;
        max-width: 32%;
        opacity: 0.95;
    }
    .hero-scene svg { width: 100%; height: auto; display: block; }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        line-height: 1.1;
        margin: 0 0 0.35rem;
        white-space: nowrap;
        background: linear-gradient(120deg, #4ADE80 0%, #22C55E 60%, #0E7C3E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero p {
        color: #94A39A;
        font-size: 1.05rem;
        line-height: 1.4;
        margin: 0;
        max-width: 58ch;
    }

    /* ---------- Cultivo icon (categoría) ---------- */
    .cultivo-head-left {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        flex: 1;
        min-width: 0;
    }
    .cultivo-icon {
        flex-shrink: 0;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(74, 222, 128, 0.08);
        border: 1px solid rgba(74, 222, 128, 0.18);
        border-radius: 10px;
    }
    .cultivo-icon svg { width: 28px; height: 28px; display: block; }

    /* ---------- Empty state illustration ---------- */
    .placeholder-illus {
        width: 100%;
        max-width: 340px;
        margin: 0 auto 1.5rem;
        opacity: 0.88;
    }
    .placeholder-illus svg { width: 100%; height: auto; display: block; }

    /* ---------- Section headings ---------- */
    .section-head {
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
        margin: 1.5rem 0 1rem;
    }
    .section-head h2 {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
        color: #E8ECE9;
    }
    .section-head .count {
        color: #94A39A;
        font-size: 1rem;
        font-weight: 500;
    }

    /* ---------- Perfil (stats row) ---------- */
    .perfil-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.75rem;
        margin: 1rem 0 2rem;
    }
    .perfil-stat {
        background: #182420;
        border: 1px solid #243530;
        border-radius: 10px;
        padding: 1rem 1.1rem;
        text-align: center;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .perfil-stat:hover {
        border-color: rgba(74, 222, 128, 0.3);
        transform: translateY(-1px);
    }
    .perfil-head {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        margin-bottom: 0.55rem;
        color: #94A39A;
    }
    .perfil-icon { width: 16px; height: 16px; opacity: 0.75; }
    .perfil-icon svg { width: 100%; height: 100%; display: block; }
    .perfil-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }
    .perfil-value {
        font-size: 1.7rem;
        font-weight: 700;
        line-height: 1;
        color: #E8ECE9;
    }
    .perfil-unit {
        font-size: 1rem;
        font-weight: 500;
        color: #94A39A;
        margin-left: 0.15rem;
    }
    .perfil-sub {
        margin-top: 0.45rem;
        font-size: 0.78rem;
        color: #4ADE80;
        min-height: 1.1em;  /* reserva espacio aunque esté vacía: cards del mismo alto */
    }

    /* ---------- Recomendado card ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        border: 1px solid #243530 !important;
        background: linear-gradient(145deg, #15201C 0%, #182420 100%);
        padding: 1.2rem 1.3rem !important;
    }
    .cultivo-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.6rem;
    }
    .cultivo-name {
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.015em;
        color: #E8ECE9;
        margin: 0;
    }
    .pauta-tema {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A39A;
        margin-bottom: 0.35rem;
    }
    .pauta-tema-icon {
        width: 1rem; height: 1rem;
        display: inline-block;
    }
    .pauta-texto {
        color: #C4CCC7;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    .sug-item, .adv-item {
        display: flex;
        align-items: flex-start;
        gap: 0.55rem;
        padding: 0.55rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .sug-item {
        background: rgba(74, 222, 128, 0.06);
        color: #E8ECE9;
        border-left: 3px solid #4ADE80;
    }
    .sug-item.verano {
        background: rgba(96, 165, 250, 0.06);
        border-left-color: #60A5FA;
    }
    .adv-item {
        background: rgba(251, 191, 36, 0.08);
        color: #FDE68A;
        border-left: 3px solid #FBBF24;
    }

    /* ---------- Badges ---------- */
    .chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }
    .chip {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .chip-green  { background: rgba(74,222,128,0.1); color:#4ADE80; border:1px solid rgba(74,222,128,0.28); }
    .chip-amber  { background: rgba(251,191,36,0.1); color:#FBBF24; border:1px solid rgba(251,191,36,0.28); }
    .chip-blue   { background: rgba(96,165,250,0.1); color:#60A5FA; border:1px solid rgba(96,165,250,0.28); }
    .chip-gray   { background: rgba(148,163,154,0.08); color:#94A39A; border:1px solid rgba(148,163,154,0.22); }

    /* ---------- Descartes ---------- */
    .motivo-group {
        background: #121A17;
        border: 1px solid #243530;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .motivo-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #243530;
    }
    .motivo-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #E8ECE9;
    }
    .motivo-dot {
        width: 0.6rem; height: 0.6rem;
        border-radius: 999px;
        display: inline-block;
    }
    .motivo-dot.epoca      { background: #94A39A; }
    .motivo-dot.luz        { background: #FBBF24; }
    .motivo-dot.espacio    { background: #60A5FA; }
    .motivo-dot.recipiente { background: #A78BFA; }
    .motivo-dot.cuidado    { background: #22D3EE; }
    .motivo-count {
        font-size: 0.78rem;
        color: #94A39A;
        background: #182420;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
    }
    .descarte-row {
        display: grid;
        grid-template-columns: 1.9rem 10rem 1fr;
        gap: 0.85rem;
        align-items: center;
        padding: 0.55rem 0;
        border-bottom: 1px dashed rgba(148,163,154,0.08);
        font-size: 0.9rem;
    }
    .descarte-row:last-child { border-bottom: none; }
    .descarte-icon {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(148, 163, 154, 0.06);
        border-radius: 7px;
        opacity: 0.85;
    }
    .descarte-icon svg { width: 20px; height: 20px; display: block; }
    .descarte-nombre {
        font-weight: 600;
        color: #E8ECE9;
    }
    .descarte-detalle {
        color: #94A39A;
        line-height: 1.45;
    }

    /* ---------- Aviso fijo ---------- */
    .aviso-fijo {
        background: rgba(96,165,250,0.04);
        border-left: 3px solid #60A5FA;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        color: #94A39A;
        font-size: 0.85rem;
        line-height: 1.45;
        margin: 0 0 1.5rem;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] { background: #0A110E; }
    [data-testid="stSidebar"] h3 { font-size: 1rem; font-weight: 700; letter-spacing: -0.01em; }
    [data-testid="stSidebar"] .stButton button { font-weight: 600; }

    /* Encabezado de la sidebar: mini-logo en tile + título + subtítulo */
    .sidebar-head {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0 0 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #243530;
    }
    .sidebar-head-icon {
        flex-shrink: 0;
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.22);
        border-radius: 11px;
    }
    .sidebar-head-icon svg { width: 30px; height: 30px; display: block; }
    .sidebar-head-text { flex: 1; min-width: 0; }
    .sidebar-head-title {
        font-size: 1.02rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #E8ECE9;
        line-height: 1.15;
        margin: 0 0 0.15rem;
    }
    .sidebar-head-sub {
        font-size: 0.78rem;
        color: #94A39A;
        line-height: 1.3;
    }

    /* ---------- Placeholder (no submission yet) ---------- */
    .placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 1rem;
        text-align: center;
        border: 1px dashed #243530;
        border-radius: 12px;
        color: #94A39A;
    }
    .placeholder-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #C4CCC7;
        margin-bottom: 0.35rem;
    }

    /* ---------- Microanimaciones ---------- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    /* Cards (recomendados) con stagger */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        animation: fadeInUp 0.35s ease both;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        border-color: rgba(74, 222, 128, 0.3) !important;
        box-shadow: 0 10px 30px rgba(74, 222, 128, 0.08);
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(1)  { animation-delay: 0.00s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(2)  { animation-delay: 0.05s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(3)  { animation-delay: 0.10s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(4)  { animation-delay: 0.15s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(5)  { animation-delay: 0.20s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(6)  { animation-delay: 0.25s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(7)  { animation-delay: 0.30s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(8)  { animation-delay: 0.35s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(9)  { animation-delay: 0.40s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(10) { animation-delay: 0.45s; }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(n+11) { animation-delay: 0.50s; }

    /* Cultivo icon pulsa al hoverear la card */
    .cultivo-icon { transition: transform 0.25s ease, background 0.25s ease; }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover .cultivo-icon {
        transform: scale(1.08);
        background: rgba(74, 222, 128, 0.14);
    }

    /* Botones del sidebar: radio consistente con el live-counter card */
    [data-testid="stSidebar"] .stButton button {
        border-radius: 12px;
        padding-top: 0.65rem;
        padding-bottom: 0.65rem;
        transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    }
    [data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(74, 222, 128, 0.3);
    }
    /* Botón secundario (reset): link discreto */
    [data-testid="stSidebar"] .stButton button[kind="secondary"] {
        background: transparent;
        color: #94A39A;
        border: 1px solid rgba(148, 163, 154, 0.22);
        font-size: 0.82rem;
        font-weight: 500;
    }
    [data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background: rgba(148, 163, 154, 0.08);
        color: #E8ECE9;
        border-color: rgba(148, 163, 154, 0.4);
    }

    /* Grupos de descarte con fade-in sutil */
    .motivo-group { animation: fadeInUp 0.3s ease both; }

    /* Descarte row con hover */
    .descarte-row {
        transition: background 0.15s ease;
        border-radius: 6px;
        padding-left: 0.45rem;
        padding-right: 0.45rem;
        margin-left: -0.45rem;
        margin-right: -0.45rem;
    }
    .descarte-row:hover { background: rgba(74, 222, 128, 0.04); }

    /* ---------- Hint "¿qué le faltaría?" en descartes ---------- */
    .descarte-hint {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        color: #4ADE80;
        font-size: 0.78rem;
        margin-top: 0.25rem;
        opacity: 0.78;
        font-style: italic;
    }
    .descarte-hint::before {
        content: "↳";
        font-style: normal;
        opacity: 0.7;
    }

    /* ---------- Live counter en la sidebar ---------- */
    .live-counter {
        background: linear-gradient(135deg, rgba(74,222,128,0.12) 0%, rgba(34,197,94,0.08) 100%);
        border: 1px solid rgba(74,222,128,0.28);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 1rem 0 0.8rem;
        text-align: center;
    }
    .live-counter-num {
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1;
        color: #4ADE80;
        letter-spacing: -0.03em;
        transition: color 0.2s ease;
    }
    .live-counter-num.zero { color: #94A39A; }
    .live-counter-text {
        font-size: 0.78rem;
        color: #C4CCC7;
        margin-top: 0.35rem;
        line-height: 1.3;
    }

    /* ---------- Responsive ---------- */
    @media (max-width: 900px) {
        .perfil-grid { grid-template-columns: repeat(2, 1fr); }
        .descarte-row {
            grid-template-columns: 1.9rem 1fr;
            row-gap: 0.1rem;
        }
        .descarte-detalle { grid-column: 2; }
        .hero h1 { font-size: 2rem; }
        .hero-scene { display: none; }  /* la escena solo tiene sentido en desktop */
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# Helpers de rendering
# ============================================================

@st.cache_data
def _cargar_catalogo():
    return cargar_cultivos(str(RUTA_CSV))


def _chip(text: str, variant: str = "gray") -> str:
    return f'<span class="chip chip-{variant}">{text}</span>'


def _section_head(icono: str, titulo: str, extra: str = "") -> None:
    extra_html = f'<span class="count">{extra}</span>' if extra else ""
    # El icon Material se renderiza con sintaxis :material/x: en st.markdown
    st.markdown(
        f'<div class="section-head">'
        f'<h2>{titulo}</h2>{extra_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# Hero + aviso
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-mark">{LOGO_SVG}</div>
        <div class="hero-text">
            <h1>Selector de cultivos</h1>
            <p>Qué cultivos entran este mes,<br>según los 5 datos de tu huerta en el AMBA.</p>
        </div>
        <div class="hero-scene">{HERO_SCENE_SVG}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="aviso-fijo">{AVISO_FIJO}</div>',
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar: formulario
# ============================================================

# Catálogo cacheado: usamos el engine en vivo en cada rerun para el contador.
try:
    _catalogo = _cargar_catalogo()
except Exception as e:  # noqa: BLE001
    st.error(f"No pude leer el catálogo: {e}")
    st.stop()


# Session state es la ÚNICA fuente de verdad para los widgets.
# Si además pasáramos `value=`/`index=` en los widgets, Streamlit lanza
# "widget was created with a default value but also had its value set via
# the Session State API". Por eso: inicializamos defaults acá antes de que
# los widgets se dibujen, y los widgets no reciben `value=`/`index=`.
_DEFAULTS_WIDGETS: dict = {
    "w_horas_sol": 5.0,
    "w_espacio": 1.0,
    "w_profundidad": 25.0,
    "w_mes": 1,
    "w_cuidado": 2,
}
# Primera carga: sembrar los defaults si no estaban.
for _k, _v in _DEFAULTS_WIDGETS.items():
    st.session_state.setdefault(_k, _v)
# Si el run anterior pidió reset, sobreescribir con defaults y ocultar resultados.
if st.session_state.pop("_reset_requested", False):
    for _k, _v in _DEFAULTS_WIDGETS.items():
        st.session_state[_k] = _v
    st.session_state.pop("show_results", None)


with st.sidebar:
    st.markdown(
        f'<div class="sidebar-head">'
        f'<div class="sidebar-head-icon">{LOGO_SVG}</div>'
        f'<div class="sidebar-head-text">'
        f'<div class="sidebar-head-title">Datos de tu huerta</div>'
        f'<div class="sidebar-head-sub">Ajustá los valores: el contador se actualiza en vivo.</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    horas_sol = st.slider(
        "Horas de sol diarias",
        min_value=0.0, max_value=12.0, step=0.5,
        help="Promedio aproximado de horas con sol directo.",
        key="w_horas_sol",
    )
    espacio_m2 = st.number_input(
        "Espacio disponible (m²)",
        min_value=0.0, step=0.1, format="%.2f",
        help="Superficie que podés dedicar a cada cultivo.",
        key="w_espacio",
    )
    profundidad_cm = st.number_input(
        "Profundidad del recipiente (cm)",
        min_value=1.0, step=1.0, format="%.0f",
        help="Si es tierra, estimá la profundidad útil.",
        key="w_profundidad",
    )
    mes = st.selectbox(
        "Mes del año",
        options=list(MESES_NOMBRE.keys()),
        format_func=lambda m: MESES_NOMBRE[m].capitalize(),
        key="w_mes",
    )
    cuidado = st.radio(
        "Frecuencia de riego posible",
        options=list(OPCIONES_CUIDADO.keys()),
        format_func=lambda c: OPCIONES_CUIDADO[c],
        key="w_cuidado",
    )

    # Motor en vivo (cada cambio de widget dispara un rerun completo).
    try:
        _resultado_live = ejecutar_motor(
            _catalogo,
            horas_sol=horas_sol,
            espacio_m2=espacio_m2,
            profundidad_cm=profundidad_cm,
            mes=mes,
            cuidado=cuidado,
        )
    except Exception as e:  # noqa: BLE001
        st.error(f"Error del motor Experta: {e}")
        st.stop()

    _n_live = len(_resultado_live["recomendados"])
    _zero_cls = " zero" if _n_live == 0 else ""
    _singular = _n_live == 1
    st.markdown(
        f'<div class="live-counter">'
        f'<div class="live-counter-num{_zero_cls}">{_n_live}</div>'
        f'<div class="live-counter-text">'
        f'{"cultivo entraría" if _singular else "cultivos entrarían"} '
        f'en tu huerta este mes'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Botón: desbloquea la vista completa la primera vez.
    _ver = st.button(
        "Ver recomendaciones",
        type="primary",
        use_container_width=True,
    )
    if _ver:
        st.session_state.show_results = True

    st.markdown("---")
    if st.button(
        "↻  Volver a los valores iniciales",
        key="reset_btn",
        use_container_width=True,
    ):
        st.session_state._reset_requested = True
        st.rerun()

    st.caption(
        ":material/info: Catálogo de 16 especies del INTA ProHuerta, "
        "validado para el AMBA."
    )


# ============================================================
# Render de resultados
# ============================================================

_ESTACION_NOMBRE = {
    12: "Verano", 1: "Verano", 2: "Verano",
    3: "Otoño", 4: "Otoño", 5: "Otoño",
    6: "Invierno", 7: "Invierno", 8: "Invierno",
    9: "Primavera", 10: "Primavera", 11: "Primavera",
}

_RIEGO_NIVEL = {1: "Bajo", 2: "Medio", 3: "Alto"}

# Versiones cortas para la sub-label del perfil (FRASE_RIEGO es demasiado
# larga para la card: hasta 29 chars con "de forma diaria o casi diaria").
_RIEGO_SUB = {
    1: "1× por semana",
    2: "2–3× por semana",
    3: "Casi a diario",
}


def _render_perfil(horas_sol, espacio_m2, profundidad_cm, mes, cuidado):
    luz_label = etiqueta_luz(horas_sol)
    st.markdown(
        f"""
        <div class="perfil-grid">
            <div class="perfil-stat">
                <div class="perfil-head">
                    <div class="perfil-icon">{PERFIL_ICON_SOL}</div>
                    <div class="perfil-label">Sol</div>
                </div>
                <div class="perfil-value">{horas_sol:g}<span class="perfil-unit">h</span></div>
                <div class="perfil-sub">{luz_label}</div>
            </div>
            <div class="perfil-stat">
                <div class="perfil-head">
                    <div class="perfil-icon">{PERFIL_ICON_ESPACIO}</div>
                    <div class="perfil-label">Espacio</div>
                </div>
                <div class="perfil-value">{espacio_m2:g}<span class="perfil-unit">m²</span></div>
                <div class="perfil-sub"></div>
            </div>
            <div class="perfil-stat">
                <div class="perfil-head">
                    <div class="perfil-icon">{PERFIL_ICON_PROFUNDIDAD}</div>
                    <div class="perfil-label">Profundidad</div>
                </div>
                <div class="perfil-value">{profundidad_cm:g}<span class="perfil-unit">cm</span></div>
                <div class="perfil-sub"></div>
            </div>
            <div class="perfil-stat">
                <div class="perfil-head">
                    <div class="perfil-icon">{PERFIL_ICON_MES}</div>
                    <div class="perfil-label">Mes</div>
                </div>
                <div class="perfil-value">{MESES_NOMBRE[mes].capitalize()}</div>
                <div class="perfil-sub">{_ESTACION_NOMBRE[mes]}</div>
            </div>
            <div class="perfil-stat">
                <div class="perfil-head">
                    <div class="perfil-icon">{PERFIL_ICON_RIEGO}</div>
                    <div class="perfil-label">Riego</div>
                </div>
                <div class="perfil-value">{_RIEGO_NIVEL[cuidado]}</div>
                <div class="perfil-sub">{_RIEGO_SUB[cuidado]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_recomendado_card(cultivo: str, resultado: dict) -> None:
    sugerencias = resultado["sugerencias"].get(cultivo, [])
    advertencias = resultado["advertencias"].get(cultivo, [])
    icono_svg = icono_cultivo(cultivo)

    with st.container(border=True):
        # Header: icono de categoría + nombre + chips de estado
        chips = [_chip("Recomendado", "green")]
        if "SUG_VERANO" in sugerencias:
            chips.append(_chip("Consejo de verano", "blue"))
        for cod in advertencias:
            if cod == "ADV_HELADA":
                chips.append(_chip("Sensible a heladas", "amber"))
            elif cod == "ADV_ALMACIGO":
                chips.append(_chip("Almácigo protegido", "amber"))
        st.markdown(
            f'<div class="cultivo-header">'
            f'<div class="cultivo-head-left">'
            f'<div class="cultivo-icon">{icono_svg}</div>'
            f'<h3 class="cultivo-name">{cultivo}</h3>'
            f'</div>'
            f'<div class="chips">{" ".join(chips)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Pautas (3 columnas con icon Material)
        pautas = resultado["pautas"].get(cultivo, [])
        orden = {"riego": 0, "mantenimiento": 1, "cosecha": 2}
        iconos_md = {
            "riego": ":material/water_drop:",
            "mantenimiento": ":material/handyman:",
            "cosecha": ":material/eco:",
        }
        pautas_ordenadas = sorted(pautas, key=lambda p: orden.get(p["tema"], 99))
        cols = st.columns(len(pautas_ordenadas)) if pautas_ordenadas else []
        for col, pauta in zip(cols, pautas_ordenadas):
            with col:
                tema = pauta["tema"]
                st.markdown(f"{iconos_md.get(tema, '')} **{TEMAS_PAUTA[tema]}**")
                kwargs = {
                    k: pauta.get(k) for k in ("p1", "p2", "p3")
                    if pauta.get(k) is not None
                }
                st.markdown(
                    f'<div class="pauta-texto">{render(pauta["codigo"], **kwargs)}</div>',
                    unsafe_allow_html=True,
                )

        # Sugerencia de inicio (todas menos SUG_VERANO)
        for codigo in sugerencias:
            if codigo == "SUG_VERANO":
                continue
            st.markdown(
                f'<div class="sug-item">'
                f'<span style="color:#4ADE80;font-weight:700;">›</span>'
                f'<span>{render(codigo)}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        # Consejo estacional de verano
        if "SUG_VERANO" in sugerencias:
            st.markdown(
                f'<div class="sug-item verano">'
                f'<span style="color:#60A5FA;font-weight:700;">◆</span>'
                f'<span>{render("SUG_VERANO")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        # Advertencias
        for codigo in advertencias:
            st.markdown(
                f'<div class="adv-item">'
                f'<span style="color:#FBBF24;font-weight:700;">⚠</span>'
                f'<span>{render(codigo)}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


def _fmt_diff(x: float) -> str:
    """Entero sin decimales si cae redondo, float con hasta 2 sin ceros extra."""
    if abs(x - round(x)) < 0.01:
        return str(int(round(x)))
    return f"{x:.2f}".rstrip("0").rstrip(".")


def _hint_descarte(motivo: str, usr, req) -> str | None:
    """Mensaje accionable: qué cambio mínimo haría entrar al cultivo.

    No aplica para 'epoca' (el detalle ya menciona los meses de siembra).
    """
    if motivo == "epoca" or usr is None or req is None:
        return None
    diff = float(req) - float(usr)
    if motivo == "luz":
        return f"Con {_fmt_diff(diff)} h más de sol, entraría."
    if motivo == "espacio":
        return f"Con {_fmt_diff(diff)} m² más de espacio, entraría."
    if motivo == "recipiente":
        return f"Con {_fmt_diff(diff)} cm más de profundidad, entraría."
    if motivo == "cuidado":
        return f"Si pudieras regar {FRASE_RIEGO[int(req)]}, entraría."
    return None


def _render_descarte_grupo(motivo: str, items: list[dict]) -> None:
    """Dibuja el grupo de descartes de un motivo con header de color."""
    titulo = MOTIVOS_DESCARTE[motivo]
    st.markdown(
        f'<div class="motivo-group">'
        f'<div class="motivo-header">'
        f'<div class="motivo-title">'
        f'<span class="motivo-dot {motivo}"></span>'
        f'<span>{titulo}</span>'
        f'</div>'
        f'<span class="motivo-count">{len(items)}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    for d in sorted(items, key=lambda x: x["cultivo"]):
        if motivo == "epoca":
            msg = render_descarte_epoca(
                d["mes"], d.get("meses_siembra"), d.get("meses_trasplante"),
            )
        else:
            msg = render_cumple_o_falla(
                d["codigo"], motivo, d.get("usr"), d.get("req"),
            )
        icono_svg = icono_cultivo(d["cultivo"])
        hint = _hint_descarte(motivo, d.get("usr"), d.get("req"))
        hint_html = f'<div class="descarte-hint">{hint}</div>' if hint else ""
        st.markdown(
            f'<div class="descarte-row">'
            f'<div class="descarte-icon">{icono_svg}</div>'
            f'<div class="descarte-nombre">{d["cultivo"]}</div>'
            f'<div class="descarte-detalle">{msg}{hint_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def _render_descartes(resultado: dict) -> None:
    por_motivo: dict[str, list[dict]] = {}
    for d in resultado["descartes"]:
        por_motivo.setdefault(d["motivo"], []).append(d)
    for motivo in ("epoca", "luz", "espacio", "recipiente", "cuidado"):
        if motivo not in por_motivo:
            continue
        _render_descarte_grupo(motivo, por_motivo[motivo])


# ============================================================
# Flujo principal
# ============================================================

if st.session_state.get("show_results"):
    resultado = _resultado_live

    # Perfil
    _section_head("", "Tu huerta")
    _render_perfil(horas_sol, espacio_m2, profundidad_cm, mes, cuidado)

    # Recomendados: una card por fila (full width).
    # Con 3 pautas en 3 columnas dentro, un card estrecho corta el texto feo.
    # Full width lee mejor, aunque implique más scroll con muchos cultivos.
    recomendados = resultado["recomendados"]
    if recomendados:
        _section_head("", "Cultivos recomendados", f"{len(recomendados)} especies")
        for cultivo in recomendados:
            _render_recomendado_card(cultivo, resultado)
    else:
        _section_head("", "Cultivos recomendados")
        st.markdown(
            f'<div class="motivo-group">'
            f'<div style="color:#FBBF24;font-weight:600;margin-bottom:0.5rem;">'
            f'⚠ Sin resultados</div>'
            f'<div style="color:#C4CCC7;">{render("MSG_SIN_RESULTADOS")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Descartados
    total_descartes = len(resultado["descartes"])
    if total_descartes:
        _section_head("", "Cultivos descartados", f"{total_descartes} hechos")
        st.caption(
            "Un mismo cultivo puede aparecer en varios motivos si falla en "
            "más de un criterio. Debajo de cada uno te decimos qué le "
            "faltaría para entrar."
        )
        _render_descartes(resultado)

else:
    st.markdown(
        f'<div class="placeholder">'
        f'<div class="placeholder-illus">{EMPTY_STATE_SVG}</div>'
        f'<div class="placeholder-title">Jugá con los valores y mirá el contador</div>'
        f'<div>Cuando quieras ver el detalle, apretá <strong>Ver recomendaciones</strong>.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
