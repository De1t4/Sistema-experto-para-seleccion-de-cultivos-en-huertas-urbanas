"""Capa de UI: todo el texto para el usuario.

Esta es la ÚNICA fuente de texto para la interfaz. El motor en
knowledge_base.py no contiene cadenas destinadas al usuario; solo emite
hechos con un codigo y datos crudos. Esta capa resuelve esos códigos
contra las plantillas de C.6 y la tabla de inicio de C.7.
"""
import re


# ---------- Códigos de cuidado (UI muestra la frase, envía el entero) ----------

OPCIONES_CUIDADO = {
    1: "Puedo regar 1 vez por semana o menos",
    2: "Puedo regar 2 o 3 veces por semana",
    3: "Puedo regar de forma diaria o casi diaria",
}


# ---------- FRASE_RIEGO: para rellenar {usr_frase} y {req_frase} ----------

FRASE_RIEGO = {
    1: "1 vez por semana o menos",
    2: "2 o 3 veces por semana",
    3: "de forma diaria o casi diaria",
}


# ---------- Etiquetas decorativas de luz (solo UI) ----------

ETIQUETAS_LUZ = {
    "baja": "Sombra parcial",
    "media": "Sol moderado",
    "alta": "Sol pleno",
}


# ---------- Nombres de los meses ----------

MESES_NOMBRE = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}


# ---------- C.7 Sugerencia de inicio: modo x metodo ----------

CODIGO_INICIO = {
    ("siembra", "directa"): "SUG_SIEMBRA_DIRECTA",
    ("siembra", "almacigo"): "SUG_SIEMBRA_ALMACIGO",
    ("siembra", "ambos"): "SUG_SIEMBRA_AMBOS",
    ("ambas", "directa"): "SUG_AMBAS_DIRECTA",
    ("ambas", "almacigo"): "SUG_AMBAS_ALMACIGO",
    ("ambas", "ambos"): "SUG_AMBAS_AMBOS",
    ("plantines", "directa"): "SUG_PLANTINES",
    ("plantines", "almacigo"): "SUG_PLANTINES",
    ("plantines", "ambos"): "SUG_PLANTINES",
}


# ---------- Aviso fijo (siempre visible en la UI) ----------

AVISO_FIJO = (
    "Esta herramienta orienta la elección de cultivos: no garantiza que "
    "un cultivo crezca, no diagnostica enfermedades ni reemplaza el "
    "consejo de un especialista."
)


# ---------- C.6 Tabla de plantillas (texto por código) ----------

PLANTILLAS = {
    # Nivel 3: Cumple y Falla por criterio
    "LUZ_OK": "Pide al menos {req} h de sol y tenés {usr} h.",
    "LUZ_FALTA": "Le faltan horas de sol: pide al menos {req} h y tenés {usr} h.",
    "ESP_OK": "Necesita {req} m² y tenés {usr} m².",
    "ESP_FALTA": "No alcanza el espacio: necesita {req} m² y tenés {usr} m².",
    "REC_OK": "Necesita {req} cm de profundidad y tu recipiente tiene {usr} cm.",
    "REC_FALTA": "El recipiente es poco profundo: necesita {req} cm y el tuyo tiene {usr} cm.",
    "CUI_OK": "Se riega {req_frase} y vos podés regar {usr_frase}.",
    "CUI_FALTA": "Se riega {req_frase}, pero vos podés regar {usr_frase}.",

    # Nivel 4: Descarte por época y SinResultados
    "DESC_EPOCA": (
        "Estamos en {mes} y no es su época: se siembra en {meses_siembra}"
        "[ y se trasplanta en {meses_trasplante}]."
    ),
    "MSG_SIN_RESULTADOS": (
        "Ningún cultivo del catálogo cumple las condiciones de tu huerta "
        "en este mes."
    ),

    # Nivel 5: Pauta de riego
    "PAU_RIEGO_1": "Regar una vez por semana.",
    "PAU_RIEGO_2": "Regar 2 o 3 veces por semana.",
    "PAU_RIEGO_3": "Regar todos los días o casi todos los días.",

    # Nivel 5: Pauta de mantenimiento y cosecha
    "PAU_MANT": "Labores: {p1}. Atención sugerida: {p2}.",
    "PAU_COS": "Hortaliza de {p3}. Manejo de cosecha: {p1}. Ciclo estimado: {p2} días.",

    # Nivel 5: Sugerencia de inicio (modo x método, R5.4)
    "SUG_SIEMBRA_DIRECTA": "Este mes podés sembrar directo en el recipiente.",
    "SUG_SIEMBRA_ALMACIGO": "Este mes podés preparar un almácigo con semillas y trasplantar después.",
    "SUG_SIEMBRA_AMBOS": (
        "Este mes podés sembrar directo en el recipiente o preparar un "
        "almácigo con semillas."
    ),
    "SUG_AMBAS_DIRECTA": (
        "Este mes podés sembrar directo en el recipiente o comprar "
        "plantines y trasplantar."
    ),
    "SUG_AMBAS_ALMACIGO": (
        "Este mes podés preparar un almácigo con semillas o comprar "
        "plantines y trasplantar."
    ),
    "SUG_AMBAS_AMBOS": (
        "Este mes podés sembrar directo, preparar un almácigo con semillas "
        "o comprar plantines y trasplantar."
    ),
    "SUG_PLANTINES": (
        "La época de siembra por semilla ya pasó, pero estás a tiempo de "
        "incorporar el cultivo comprando plantines para trasplantar este mes."
    ),

    # Nivel 5: consejo estacional y advertencias
    "SUG_VERANO": "Es verano: protegé el suelo de la evaporación.",
    "ADV_ALMACIGO": "Mantené el almácigo protegido del frío.",
    "ADV_HELADA": "Es sensible a heladas: protegelo en las noches frías.",
}


# ---------- Rendering ----------

MOTIVOS_DESCARTE = {
    "epoca": "No es su época",
    "luz": "Le faltan horas de sol",
    "espacio": "No alcanza el espacio",
    "recipiente": "El recipiente es poco profundo",
    "cuidado": "No podés regarla con la frecuencia que necesita",
}

TEMAS_PAUTA = {
    "riego": "Riego",
    "mantenimiento": "Mantenimiento",
    "cosecha": "Cosecha",
}


def _formatear_lista_meses(meses):
    """Convierte un frozenset de ints 1-12 en 'enero, febrero, …' ordenada."""
    if not meses:
        return ""
    return ", ".join(MESES_NOMBRE[m] for m in sorted(meses))


def _formato_num(x):
    """Mostrar enteros sin decimales y floats con hasta 2 decimales, sin ceros extra."""
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, float):
        if x.is_integer():
            return str(int(x))
        return f"{x:.2f}".rstrip("0").rstrip(".")
    return str(x)


def _expandir_opcionales(tpl: str, datos: dict) -> str:
    """Resuelve segmentos [opcionales]: se omiten si falta algún dato."""
    def repl(match):
        seg = match.group(1)
        vars_in = re.findall(r"\{(\w+)\}", seg)
        if any(not datos.get(v) for v in vars_in):
            return ""
        return seg
    return re.sub(r"\[([^\[\]]+)\]", repl, tpl)


def render(codigo: str, **datos) -> str:
    """Rinde una plantilla C.6 con los datos ya formateados."""
    tpl = PLANTILLAS[codigo]
    tpl = _expandir_opcionales(tpl, datos)
    return tpl.format_map({k: _formato_num(v) for k, v in datos.items()})


def render_cumple_o_falla(codigo: str, criterio: str, usr, req) -> str:
    """Rinde una línea Cumple/Falla con los valores crudos del motor."""
    if criterio == "cuidado":
        return render(
            codigo,
            usr_frase=FRASE_RIEGO[int(usr)],
            req_frase=FRASE_RIEGO[int(req)],
        )
    return render(codigo, usr=usr, req=req)


def render_descarte_epoca(mes_int: int, meses_siembra, meses_trasplante) -> str:
    """Rinde el mensaje DESC_EPOCA, convirtiendo meses a texto."""
    return render(
        "DESC_EPOCA",
        mes=MESES_NOMBRE[int(mes_int)],
        meses_siembra=_formatear_lista_meses(meses_siembra or frozenset()),
        meses_trasplante=_formatear_lista_meses(meses_trasplante or frozenset()),
    )


def etiqueta_luz(horas: float) -> str:
    """Devuelve la etiqueta decorativa correspondiente a las horas de sol."""
    if horas < 3:
        return ETIQUETAS_LUZ["baja"]
    if horas <= 5:
        return ETIQUETAS_LUZ["media"]
    return ETIQUETAS_LUZ["alta"]
