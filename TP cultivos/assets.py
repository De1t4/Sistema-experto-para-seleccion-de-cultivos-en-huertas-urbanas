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


# ============================================================
# Un icono por cultivo del catálogo v6
# ============================================================

# Acelga: hojas verdes anchas sobre pencas blancas verticales.
_ICON_ACELGA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <rect x="14" y="14" width="4" height="16" fill="#F3F4F6" rx="2"/>
    <path d="M14 16 Q 4 12, 2 4 Q 12 6, 14 14 Z" fill="#15803D"/>
    <path d="M18 16 Q 28 12, 30 4 Q 20 6, 18 14 Z" fill="#166534"/>
</svg>"""

# Albahaca: pares de hojas pequeñas redondeadas sobre un tallo corto.
_ICON_ALBAHACA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 28 L 16 10" stroke="#166534" stroke-width="1.5" stroke-linecap="round"/>
    <ellipse cx="10" cy="20" rx="4" ry="2.5" fill="#4ADE80" transform="rotate(-25 10 20)"/>
    <ellipse cx="22" cy="20" rx="4" ry="2.5" fill="#4ADE80" transform="rotate(25 22 20)"/>
    <ellipse cx="11" cy="13" rx="3.5" ry="2.2" fill="#22C55E" transform="rotate(-30 11 13)"/>
    <ellipse cx="21" cy="13" rx="3.5" ry="2.2" fill="#22C55E" transform="rotate(30 21 13)"/>
    <ellipse cx="16" cy="6" rx="2.5" ry="3.5" fill="#86EFAC"/>
</svg>"""

# Apio: 3 pencas pálidas con copo de hojas verdes arriba.
_ICON_APIO = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 12 Q 16 2, 26 12 Q 16 16, 6 12 Z" fill="#15803D"/>
    <rect x="10" y="12" width="3" height="18" fill="#86EFAC" rx="1.5"/>
    <rect x="14.5" y="12" width="3" height="18" fill="#A7F3D0" rx="1.5"/>
    <rect x="19" y="12" width="3" height="18" fill="#86EFAC" rx="1.5"/>
    <line x1="11.5" y1="14" x2="11.5" y2="28" stroke="#15803D" stroke-width="0.4"/>
    <line x1="16" y1="14" x2="16" y2="28" stroke="#15803D" stroke-width="0.4"/>
    <line x1="20.5" y1="14" x2="20.5" y2="28" stroke="#15803D" stroke-width="0.4"/>
</svg>"""

# Calabaza: cuerpo naranja con costillas verticales y pedúnculo verde.
_ICON_CALABAZA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="16" cy="20" rx="12" ry="10" fill="#F97316"/>
    <path d="M10 11 Q 7 20, 10 29" stroke="#C2410C" stroke-width="0.9" fill="none" opacity="0.6"/>
    <path d="M16 10 L 16 30" stroke="#C2410C" stroke-width="0.9" fill="none" opacity="0.6"/>
    <path d="M22 11 Q 25 20, 22 29" stroke="#C2410C" stroke-width="0.9" fill="none" opacity="0.6"/>
    <path d="M14 10 L 14 6 Q 16 4, 18 6 L 18 10 Z" fill="#15803D"/>
    <ellipse cx="12" cy="16" rx="1.5" ry="2.5" fill="#FDBA74" opacity="0.5"/>
</svg>"""

# Espinaca: hojas verde oscuro, forma puntiaguda, en manojo.
_ICON_ESPINACA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 30 Q 10 22, 10 10 Q 14 4, 16 14 Q 18 4, 22 10 Q 22 22, 16 30 Z" fill="#15803D"/>
    <path d="M10 24 Q 4 20, 4 12 Q 9 10, 10 20 Z" fill="#166534"/>
    <path d="M22 24 Q 28 20, 28 12 Q 23 10, 22 20 Z" fill="#166534"/>
    <line x1="16" y1="14" x2="16" y2="28" stroke="#14532D" stroke-width="0.6"/>
</svg>"""

# Haba: chaucha verde con 3 semillas visibles.
_ICON_HABA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 20 Q 2 10, 10 8 Q 20 2, 28 10 Q 30 20, 22 24 Q 10 30, 4 20 Z" fill="#4ADE80"/>
    <path d="M6 18 Q 8 12, 14 10" stroke="#22C55E" stroke-width="0.7" fill="none"/>
    <ellipse cx="11" cy="18" rx="2.5" ry="2" fill="#166534"/>
    <ellipse cx="17" cy="16" rx="2.5" ry="2" fill="#166534"/>
    <ellipse cx="23" cy="14" rx="2.5" ry="2" fill="#166534"/>
</svg>"""

# Lechuga: cabeza redonda, hojas verdes superpuestas en capas.
_ICON_LECHUGA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="17" r="12" fill="#86EFAC"/>
    <circle cx="12" cy="14" r="5" fill="#22C55E"/>
    <circle cx="20" cy="14" r="5" fill="#22C55E"/>
    <circle cx="10" cy="20" r="4.5" fill="#4ADE80"/>
    <circle cx="22" cy="20" r="4.5" fill="#4ADE80"/>
    <circle cx="16" cy="18" r="5" fill="#15803D"/>
</svg>"""

# Maíz dulce: choclo amarillo con granos y hojas verdes a los costados.
_ICON_MAIZ = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 10 Q 5 14, 7 25 Q 11 26, 12 20 Z" fill="#22C55E"/>
    <path d="M20 10 Q 27 14, 25 25 Q 21 26, 20 20 Z" fill="#22C55E"/>
    <path d="M13 5 L 13 8 M 16 3 L 16 8 M 19 5 L 19 8" stroke="#FBBF24" stroke-width="1.2" stroke-linecap="round"/>
    <path d="M11 7 Q 16 3, 21 7" stroke="#FBBF24" stroke-width="1" stroke-linecap="round" fill="none"/>
    <rect x="12" y="8" width="8" height="20" rx="3" fill="#FDE047"/>
    <circle cx="14" cy="12" r="0.9" fill="#CA8A04"/><circle cx="16" cy="12" r="0.9" fill="#CA8A04"/><circle cx="18" cy="12" r="0.9" fill="#CA8A04"/>
    <circle cx="14" cy="15" r="0.9" fill="#CA8A04"/><circle cx="16" cy="15" r="0.9" fill="#CA8A04"/><circle cx="18" cy="15" r="0.9" fill="#CA8A04"/>
    <circle cx="14" cy="18" r="0.9" fill="#CA8A04"/><circle cx="16" cy="18" r="0.9" fill="#CA8A04"/><circle cx="18" cy="18" r="0.9" fill="#CA8A04"/>
    <circle cx="14" cy="21" r="0.9" fill="#CA8A04"/><circle cx="16" cy="21" r="0.9" fill="#CA8A04"/><circle cx="18" cy="21" r="0.9" fill="#CA8A04"/>
    <circle cx="14" cy="24" r="0.9" fill="#CA8A04"/><circle cx="16" cy="24" r="0.9" fill="#CA8A04"/><circle cx="18" cy="24" r="0.9" fill="#CA8A04"/>
</svg>"""

# Melón: esfera beige-marrón con red característica.
_ICON_MELON = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="18" r="11" fill="#D6D3D1"/>
    <path d="M6 14 Q 16 11, 26 14" stroke="#78716C" stroke-width="0.6" fill="none"/>
    <path d="M6 18 Q 16 15, 26 18" stroke="#78716C" stroke-width="0.6" fill="none"/>
    <path d="M6 22 Q 16 19, 26 22" stroke="#78716C" stroke-width="0.6" fill="none"/>
    <path d="M10 9 Q 12 20, 10 28" stroke="#78716C" stroke-width="0.5" fill="none" opacity="0.7"/>
    <path d="M22 9 Q 20 20, 22 28" stroke="#78716C" stroke-width="0.5" fill="none" opacity="0.7"/>
    <path d="M14 8 L 14 5 Q 16 4, 18 5 L 18 8" fill="#15803D"/>
</svg>"""

# Pepino: fruto alargado verde oscuro, texturas de bultitos.
_ICON_PEPINO = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="16" cy="17" rx="5" ry="12" fill="#22C55E"/>
    <path d="M12 6 Q 16 4, 20 6 Q 20 10, 16 10 Q 12 10, 12 6 Z" fill="#15803D"/>
    <path d="M15 5 L 15 2" stroke="#15803D" stroke-width="1" stroke-linecap="round"/>
    <circle cx="13" cy="12" r="0.7" fill="#166534" opacity="0.7"/>
    <circle cx="18" cy="14" r="0.7" fill="#166534" opacity="0.7"/>
    <circle cx="14" cy="18" r="0.7" fill="#166534" opacity="0.7"/>
    <circle cx="17" cy="22" r="0.7" fill="#166534" opacity="0.7"/>
    <circle cx="15" cy="26" r="0.7" fill="#166534" opacity="0.7"/>
    <ellipse cx="13" cy="17" rx="0.8" ry="7" fill="#4ADE80" opacity="0.5"/>
</svg>"""

# Perejil: ramillete de hojitas tupidas sobre tallo corto.
_ICON_PEREJIL = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 30 L 16 20" stroke="#166534" stroke-width="1.5" stroke-linecap="round"/>
    <circle cx="12" cy="14" r="3.5" fill="#22C55E"/>
    <circle cx="20" cy="14" r="3.5" fill="#22C55E"/>
    <circle cx="16" cy="18" r="3.5" fill="#15803D"/>
    <circle cx="14" cy="9" r="3" fill="#4ADE80"/>
    <circle cx="18" cy="9" r="3" fill="#4ADE80"/>
    <circle cx="16" cy="5" r="2.5" fill="#86EFAC"/>
</svg>"""

# Rabanito: bulbo rojo con hojas verdes arriba y punta de raíz.
_ICON_RABANITO = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="22" r="7" fill="#DC2626"/>
    <ellipse cx="16" cy="26" rx="6" ry="2" fill="#991B1B" opacity="0.5"/>
    <path d="M16 29 L 15 32" stroke="#991B1B" stroke-width="1" stroke-linecap="round"/>
    <ellipse cx="13" cy="20" rx="1.5" ry="2" fill="#F87171" opacity="0.6"/>
    <path d="M10 11 Q 16 6, 22 11 Q 22 15, 16 15 Q 10 15, 10 11 Z" fill="#15803D"/>
    <path d="M12 8 Q 14 3, 16 7 M 16 7 Q 18 3, 20 8" stroke="#22C55E" stroke-width="1.5" stroke-linecap="round" fill="none"/>
</svg>"""

# Rúcula: hoja dentada alargada, verde oscuro, con nervadura.
_ICON_RUCULA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 30 Q 11 22, 11 16 L 8 14 L 11 13 L 10 10 L 13 10 L 13 7 L 16 9 L 19 7 L 19 10 L 22 10 L 21 13 L 24 14 L 21 16 Q 21 22, 16 30 Z" fill="#166534"/>
    <path d="M16 12 L 16 28" stroke="#14532D" stroke-width="0.7"/>
    <path d="M10 24 Q 7 20, 7 14 L 10 16 Z" fill="#15803D" opacity="0.6"/>
</svg>"""

# Tomate: fruto rojo con sépalo estrellado verde y pedúnculo.
_ICON_TOMATE = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="19" r="11" fill="#DC2626"/>
    <ellipse cx="12" cy="14" rx="2.5" ry="2" fill="#F87171" opacity="0.7"/>
    <path d="M16 10 Q 14 20, 16 29" stroke="#991B1B" stroke-width="0.5" fill="none" opacity="0.4"/>
    <path d="M16 10 Q 18 20, 16 29" stroke="#991B1B" stroke-width="0.5" fill="none" opacity="0.4"/>
    <path d="M16 10 L 11 7 L 13 10 L 10 11 L 13 12 L 11 15 L 16 12 L 21 15 L 19 12 L 22 11 L 19 10 L 21 7 Z" fill="#15803D"/>
    <path d="M16 10 L 16 5" stroke="#15803D" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""

# Zanahoria: raíz triangular naranja con penachos verdes.
_ICON_ZANAHORIA = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 12 L 22 12 L 17 29 Q 16 30, 15 29 Z" fill="#F97316"/>
    <line x1="11" y1="16" x2="21" y2="16" stroke="#C2410C" stroke-width="0.5"/>
    <line x1="12" y1="20" x2="20" y2="20" stroke="#C2410C" stroke-width="0.5"/>
    <line x1="13" y1="24" x2="19" y2="24" stroke="#C2410C" stroke-width="0.5"/>
    <path d="M10 12 Q 11 4, 13 11 M 13 11 Q 15 2, 16 10 M 16 10 Q 17 2, 19 11 M 19 11 Q 21 4, 22 12" stroke="#22C55E" stroke-width="2" stroke-linecap="round" fill="none"/>
</svg>"""

# Zapallito: fruto redondo verde con costillas y pedúnculo chico.
_ICON_ZAPALLITO = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="20" r="9" fill="#22C55E"/>
    <path d="M11 13 Q 10 20, 11 27" stroke="#15803D" stroke-width="0.6" fill="none" opacity="0.7"/>
    <path d="M16 11 Q 16 20, 16 29" stroke="#15803D" stroke-width="0.4" fill="none" opacity="0.5"/>
    <path d="M21 13 Q 22 20, 21 27" stroke="#15803D" stroke-width="0.6" fill="none" opacity="0.7"/>
    <path d="M14 11 L 14 7 Q 16 5, 18 7 L 18 11 Z" fill="#166534"/>
    <ellipse cx="12" cy="17" rx="1" ry="2.5" fill="#86EFAC" opacity="0.5"/>
</svg>"""

# Fallback neutral: usado si el catálogo trae un nombre que no tiene icono.
_ICON_GENERICO = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M5 5 Q 20 4, 27 14 Q 29 24, 16 29 Q 4 26, 5 14 Z" fill="#4ADE80" opacity="0.9"/>
    <path d="M5 5 Q 14 14, 24 26" stroke="#15803D" stroke-width="1.4" fill="none" opacity="0.7"/>
</svg>"""


CULTIVO_ICONS: dict[str, str] = {
    "Acelga": _ICON_ACELGA,
    "Albahaca": _ICON_ALBAHACA,
    "Apio": _ICON_APIO,
    "Calabaza": _ICON_CALABAZA,
    "Espinaca": _ICON_ESPINACA,
    "Haba": _ICON_HABA,
    "Lechuga": _ICON_LECHUGA,
    "Maíz dulce": _ICON_MAIZ,
    "Melón": _ICON_MELON,
    "Pepino": _ICON_PEPINO,
    "Perejil": _ICON_PEREJIL,
    "Rabanito": _ICON_RABANITO,
    "Rúcula": _ICON_RUCULA,
    "Tomate": _ICON_TOMATE,
    "Zanahoria": _ICON_ZANAHORIA,
    "Zapallito": _ICON_ZAPALLITO,
}


def icono_cultivo(nombre: str) -> str:
    """SVG inline del icono por nombre de cultivo (match exacto con el CSV).

    Si el catálogo trae un nombre que no está en CULTIVO_ICONS, devuelve
    un icono genérico de hoja verde (no rompe la UI).
    """
    return CULTIVO_ICONS.get(nombre, _ICON_GENERICO)


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
