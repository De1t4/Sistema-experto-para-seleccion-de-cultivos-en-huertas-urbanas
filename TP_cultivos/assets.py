"""Assets SVG inline para la UI.

Todo inline: cero dependencias externas, funciona offline, no requiere
subir archivos al deploy.

Convenciones:
  - Todos los iconos de cultivo son viewBox 32x32, flat colors, 2-5
    shapes cada uno. Diseñados para leer bien a 28x28 pixel real
    (el tamaño que usa el tile de las cards y de los descartes).
  - Paleta coherente con el theme principal:
      verdes:  #86EFAC, #4ADE80, #22C55E, #15803D, #166534, #14532D
      naranjas:#FDBA74, #F97316, #C2410C
      rojos:   #F87171, #DC2626, #991B1B
      amarillo:#FDE047, #FBBF24, #CA8A04
      tierra:  #8B6F47
      neutro:  #D6D3D1, #F3F4F6
"""


# ============================================================
# Logo del proyecto (hero)
# ============================================================

LOGO_SVG = """<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="leaf-l" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#4ADE80"/>
            <stop offset="1" stop-color="#15803D"/>
        </linearGradient>
        <linearGradient id="leaf-r" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#86EFAC"/>
            <stop offset="1" stop-color="#22C55E"/>
        </linearGradient>
    </defs>
    <path d="M24 44 Q 24 32, 24 24" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    <path d="M24 26 Q 10 24, 4 12 Q 16 14, 24 26 Z" fill="url(#leaf-l)"/>
    <path d="M24 26 Q 38 24, 44 12 Q 32 14, 24 26 Z" fill="url(#leaf-r)"/>
    <ellipse cx="24" cy="44" rx="14" ry="1.5" fill="#8B6F47" opacity="0.35"/>
</svg>"""


# ============================================================
# Ilustración del empty state (placeholder antes del submit)
# ============================================================

EMPTY_STATE_SVG = """<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0" stop-color="#FBBF24" stop-opacity="0.6"/>
            <stop offset="1" stop-color="#FBBF24" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="leaf-small" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#86EFAC"/>
            <stop offset="1" stop-color="#15803D"/>
        </linearGradient>
    </defs>
    <circle cx="340" cy="45" r="42" fill="url(#sun)"/>
    <circle cx="340" cy="45" r="13" fill="#FBBF24" opacity="0.75"/>
    <path d="M60 135 L 340 135 L 320 185 L 80 185 Z" fill="#2D1F14" opacity="0.55"/>
    <path d="M60 135 L 340 135 L 338 143 L 62 143 Z" fill="#8B6F47" opacity="0.5"/>
    <g transform="translate(130, 90)">
        <path d="M0 50 Q 0 25, 0 15" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M0 20 Q -14 15, -16 2 Q -4 5, 0 20 Z" fill="url(#leaf-small)"/>
        <path d="M0 20 Q 14 15, 16 2 Q 4 5, 0 20 Z" fill="url(#leaf-small)"/>
    </g>
    <g transform="translate(200, 75)">
        <path d="M0 60 Q 0 32, 0 18" stroke="#22C55E" stroke-width="3" stroke-linecap="round" fill="none"/>
        <path d="M0 24 Q -18 18, -20 2 Q -5 6, 0 24 Z" fill="url(#leaf-small)"/>
        <path d="M0 24 Q 18 18, 20 2 Q 5 6, 0 24 Z" fill="url(#leaf-small)"/>
    </g>
    <g transform="translate(270, 95)">
        <path d="M0 45 Q 0 22, 0 12" stroke="#22C55E" stroke-width="2.3" stroke-linecap="round" fill="none"/>
        <path d="M0 17 Q -12 12, -14 1 Q -3 4, 0 17 Z" fill="url(#leaf-small)"/>
        <path d="M0 17 Q 12 12, 14 1 Q 3 4, 0 17 Z" fill="url(#leaf-small)"/>
    </g>
</svg>"""
import base64
from pathlib import Path
import re
import unicodedata

# 1. Definir la ruta relativa hacia la carpeta de imágenes PNG
# Path(__file__).resolve().parent obtiene la carpeta donde vive assets.py
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "assets" / "cultivos-png"


def _slug(nombre: str) -> str:
    """Normaliza nombres: 'Maíz dulce' -> 'maiz_dulce-v2'."""
    s = (
        unicodedata.normalize("NFD", nombre.lower())
        .encode("ascii", "ignore")
        .decode()
    )
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return f"{s}-v2"

# ============================================================
# Un icono por cultivo del catálogo v6
# ============================================================

# 2. Cargar en memoria todas las imágenes PNG convertidas a Base64
CULTIVO_ICONS: dict[str, str] = {}

if IMG_DIR.exists():
    for p in IMG_DIR.glob("*.png"):
        CULTIVO_ICONS[p.stem] = (
            "data:image/png;base64,"
            + base64.b64encode(p.read_bytes()).decode()
        )

# Respaldo visual (fallback) en HTML si no existe la imagen
_ICON_GENERICO = '<div style="font-size:45px; text-align:center;">🌱</div>'

def icono_cultivo(nombre: str) -> str:
    """Devuelve la etiqueta HTML <img ...> lista para renderizar en app.py.

    Mantiene la misma firma para no romper las llamadas existentes.
    """
    key = _slug(nombre)
    src = CULTIVO_ICONS.get(key)

    if src:
        return (
            f'<img src="{src}" alt="{nombre}" '
            f'style="width:100%; height:100%; object-fit:contain; display:block; margin:auto;">'
        )

    return _ICON_GENERICO


# ============================================================
# Iconos chicos para la fila de perfil (sol, espacio, prof, mes, riego)
# viewBox 20x20, mono-color: usar `currentColor` así heredan del CSS.
# ============================================================

PERFIL_ICON_SOL = """<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <circle cx="10" cy="10" r="3.5" fill="currentColor"/>
    <g stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <line x1="10" y1="2" x2="10" y2="4"/>
        <line x1="10" y1="16" x2="10" y2="18"/>
        <line x1="2" y1="10" x2="4" y2="10"/>
        <line x1="16" y1="10" x2="18" y2="10"/>
        <line x1="4.2" y1="4.2" x2="5.6" y2="5.6"/>
        <line x1="14.4" y1="14.4" x2="15.8" y2="15.8"/>
        <line x1="4.2" y1="15.8" x2="5.6" y2="14.4"/>
        <line x1="14.4" y1="5.6" x2="15.8" y2="4.2"/>
    </g>
</svg>"""

PERFIL_ICON_ESPACIO = """<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <rect x="2.5" y="2.5" width="15" height="15" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2.5 2"/>
    <rect x="7" y="7" width="6" height="6" rx="1" fill="currentColor" opacity="0.35"/>
</svg>"""

PERFIL_ICON_PROFUNDIDAD = """<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <line x1="4" y1="3.5" x2="16" y2="3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
    <line x1="10" y1="3.5" x2="10" y2="14" stroke="currentColor" stroke-width="1.4"/>
    <path d="M6 12 L 10 16.5 L 14 12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

PERFIL_ICON_MES = """<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="4.5" width="14" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <line x1="3" y1="8.5" x2="17" y2="8.5" stroke="currentColor" stroke-width="1.4"/>
    <line x1="7" y1="2.5" x2="7" y2="5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    <line x1="13" y1="2.5" x2="13" y2="5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    <circle cx="10" cy="12.5" r="1.2" fill="currentColor"/>
</svg>"""

PERFIL_ICON_RIEGO = """<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 2.5 C 6.5 8, 4.5 11, 4.5 13 C 4.5 16, 7 18, 10 18 C 13 18, 15.5 16, 15.5 13 C 15.5 11, 13.5 8, 10 2.5 Z" fill="currentColor"/>
</svg>"""


# ============================================================
# Escena del hero: panorama horizontal de huerta.
# Sol a la derecha + 4 brotes de distintas alturas + nubes muy sutiles
# + línea de tierra ondulada. Mismo lenguaje gráfico que el empty state
# (misma paleta, mismos gradientes, mismo trazo).
# ============================================================

HERO_SCENE_SVG = """<svg viewBox="0 0 400 110" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="hero-sun" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0" stop-color="#FBBF24" stop-opacity="0.55"/>
            <stop offset="1" stop-color="#FBBF24" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="hero-leaf" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#86EFAC"/>
            <stop offset="1" stop-color="#15803D"/>
        </linearGradient>
    </defs>
    <circle cx="340" cy="40" r="36" fill="url(#hero-sun)"/>
    <circle cx="340" cy="40" r="12" fill="#FBBF24" opacity="0.75"/>
    <g opacity="0.14" fill="#E8ECE9">
        <circle cx="55" cy="28" r="8"/>
        <circle cx="68" cy="24" r="10"/>
        <circle cx="80" cy="28" r="7"/>
        <circle cx="46" cy="30" r="6"/>
    </g>
    <g opacity="0.11" fill="#E8ECE9">
        <circle cx="195" cy="20" r="7"/>
        <circle cx="206" cy="18" r="8"/>
        <circle cx="216" cy="21" r="6"/>
    </g>
    <path d="M 0 102 Q 100 97, 200 102 Q 300 107, 400 102" stroke="#8B6F47" stroke-width="1.2" fill="none" opacity="0.32"/>
    <g transform="translate(90, 77)">
        <path d="M0 25 Q 0 15, 0 8" stroke="#22C55E" stroke-width="2" stroke-linecap="round" fill="none"/>
        <path d="M0 12 Q -10 8, -11 0 Q -3 2, 0 12 Z" fill="url(#hero-leaf)"/>
        <path d="M0 12 Q 10 8, 11 0 Q 3 2, 0 12 Z" fill="url(#hero-leaf)"/>
    </g>
    <g transform="translate(165, 65)">
        <path d="M0 37 Q 0 20, 0 10" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M0 15 Q -14 10, -16 -2 Q -4 1, 0 15 Z" fill="url(#hero-leaf)"/>
        <path d="M0 15 Q 14 10, 16 -2 Q 4 1, 0 15 Z" fill="url(#hero-leaf)"/>
    </g>
    <g transform="translate(240, 48)">
        <path d="M0 54 Q 0 28, 0 14" stroke="#22C55E" stroke-width="3" stroke-linecap="round" fill="none"/>
        <path d="M0 22 Q -18 15, -20 0 Q -5 4, 0 22 Z" fill="url(#hero-leaf)"/>
        <path d="M0 22 Q 18 15, 20 0 Q 5 4, 0 22 Z" fill="url(#hero-leaf)"/>
    </g>
    <g transform="translate(300, 75)">
        <path d="M0 27 Q 0 17, 0 7" stroke="#22C55E" stroke-width="2" stroke-linecap="round" fill="none"/>
        <path d="M0 11 Q -11 7, -12 -2 Q -3 1, 0 11 Z" fill="url(#hero-leaf)"/>
        <path d="M0 11 Q 11 7, 12 -2 Q 3 1, 0 11 Z" fill="url(#hero-leaf)"/>
    </g>
</svg>"""
