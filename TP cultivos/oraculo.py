"""Oráculo: implementación independiente de las reglas, en Python puro.

Codifica las mismas 25 reglas lógicas del PDF (secciones C.1 a C.5) pero
SIN motor de reglas: solo iteración lineal y comparaciones directas.
Cumple dos funciones:

  1. Contraste independiente del motor Experta. Un barrido grande que
     compare ambos permite detectar bugs en knowledge_base.py que los 6
     casos CP del PDF no exceden.
  2. Respaldo de deploy. Experta 1.9.4 depende de frozendict 1.2 (sin
     wheels nativos para Python 3.12+). Si el stack de Streamlit Cloud
     cambia y Experta deja de funcionar, el oráculo mantiene la demo viva.

Estructura del output: idéntica a knowledge_base.ejecutar_motor para que
la comparación sea una diferencia de diccionarios. No produce trazas de
reglas (no es un motor de reglas) ni los hechos Cumple intermedios.
"""
from __future__ import annotations

from textos import CODIGO_INICIO


# ---------- R1.3: mes -> estación ----------

ESTACION_POR_MES = {
    12: "verano", 1: "verano", 2: "verano",
    3: "otoño", 4: "otoño", 5: "otoño",
    6: "invierno", 7: "invierno", 8: "invierno",
    9: "primavera", 10: "primavera", 11: "primavera",
}


# ---------- R1.4: modo de vigencia ----------

def _modo_vigencia(mes: int, meses_siembra, meses_trasplante) -> str | None:
    """R1.4a/b/c. Devuelve 'siembra', 'ambas', 'plantines' o None.

    None significa que el mes no está en ninguna ventana: R4.3 lo descarta
    por época.
    """
    en_siembra = mes in meses_siembra
    en_trasplante = mes in meses_trasplante
    if en_siembra and not en_trasplante:
        return "siembra"
    if en_siembra and en_trasplante:
        return "ambas"
    if not en_siembra and en_trasplante:
        return "plantines"
    return None


# ---------- R3.1-R3.8: criterios numéricos ----------

CRITERIOS = (
    # (nombre, atributo_perfil, atributo_cultivo, codigo_ok, codigo_falta)
    ("luz", "horas_sol", "horas_sol_min", "LUZ_OK", "LUZ_FALTA"),
    ("espacio", "espacio_m2", "espacio_necesario_m2", "ESP_OK", "ESP_FALTA"),
    ("recipiente", "profundidad_cm", "profundidad_min_cm", "REC_OK", "REC_FALTA"),
    ("cuidado", "cuidado", "riego_num", "CUI_OK", "CUI_FALTA"),
)


def _evaluar_criterios(perfil: dict, cultivo: dict) -> list[dict]:
    """Para un cultivo en temporada, devuelve la lista de criterios que fallan.

    Cada entrada: {criterio, codigo, usr, req}. Comparación numérica
    estricta en los cuatro criterios: Falla si usr < req; Cumple si usr >= req.
    """
    fallas = []
    for criterio, attr_perfil, attr_cultivo, _, codigo_falta in CRITERIOS:
        usr = perfil[attr_perfil]
        req = cultivo[attr_cultivo]
        if usr < req:
            fallas.append({
                "criterio": criterio, "codigo": codigo_falta,
                "usr": usr, "req": req,
            })
    return fallas


# ---------- API pública: ejecutar_oraculo ----------

def ejecutar_oraculo(
    cultivos: list[dict],
    horas_sol: float,
    espacio_m2: float,
    profundidad_cm: float,
    mes: int,
    cuidado: int,
) -> dict:
    """Clasifica el catálogo con las mismas reglas que el motor Experta.

    Devuelve un dict con las mismas claves observables que
    knowledge_base.ejecutar_motor:
      recomendados, descartes, pautas, sugerencias, advertencias,
      sin_resultados.

    No devuelve traza_global ni traza_por_cultivo (el oráculo no es un
    motor de reglas).
    """
    horas_sol = float(horas_sol)
    espacio_m2 = float(espacio_m2)
    profundidad_cm = float(profundidad_cm)
    mes = int(mes)
    cuidado = int(cuidado)

    perfil = {
        "horas_sol": horas_sol,
        "espacio_m2": espacio_m2,
        "profundidad_cm": profundidad_cm,
        "cuidado": cuidado,
    }
    estacion = ESTACION_POR_MES[mes]

    recomendados: list[str] = []
    descartes: list[dict] = []
    pautas: dict[str, list[dict]] = {}
    sugerencias: dict[str, list[str]] = {}
    advertencias: dict[str, list[str]] = {}

    for c in cultivos:
        nombre = c["nombre"]
        modo = _modo_vigencia(mes, c["meses_siembra"], c["meses_trasplante"])

        # R4.3: fuera de temporada -> descarte por época. Nivel 3 no corre.
        if modo is None:
            descartes.append({
                "cultivo": nombre, "motivo": "epoca", "codigo": "DESC_EPOCA",
                "mes": mes,
                "meses_siembra": c["meses_siembra"],
                "meses_trasplante": c["meses_trasplante"],
            })
            continue

        # Nivel 3 + R4.2: cada criterio que falla emite su propio descarte.
        fallas = _evaluar_criterios(perfil, c)
        if fallas:
            for f in fallas:
                descartes.append({
                    "cultivo": nombre, "motivo": f["criterio"],
                    "codigo": f["codigo"], "usr": f["usr"], "req": f["req"],
                })
            continue

        # R4.1: pasó los cuatro criterios -> Recomendación.
        recomendados.append(nombre)

        # Nivel 5 (solo para recomendados)
        # R5.1 Pauta de riego
        pautas.setdefault(nombre, []).append({
            "cultivo": nombre, "tema": "riego",
            "codigo": f"PAU_RIEGO_{c['riego_num']}",
        })
        # R5.2 Pauta de mantenimiento
        pautas.setdefault(nombre, []).append({
            "cultivo": nombre, "tema": "mantenimiento", "codigo": "PAU_MANT",
            "p1": c["labores_mantenimiento"],
            "p2": c["frecuencia_atencion_huerta"],
        })
        # R5.3 Pauta de cosecha
        pautas.setdefault(nombre, []).append({
            "cultivo": nombre, "tema": "cosecha", "codigo": "PAU_COS",
            "p1": c["tipo_cosecha_manejo"],
            "p2": c["dias_cosecha"],
            "p3": c["tipo_hortaliza"],
        })
        # R5.4 Sugerencia de inicio (tabla C.7 modo x metodo)
        sugerencias.setdefault(nombre, []).append(
            CODIGO_INICIO[(modo, c["metodo_siembra"])]
        )
        # R5.5 ADV_ALMACIGO (si corresponde y modo != plantines)
        if c["almacigo_protegido"] and modo != "plantines":
            advertencias.setdefault(nombre, []).append("ADV_ALMACIGO")
        # R5.6 ADV_HELADA (sensible + estación invierno + estaciones incluye invierno)
        if (
            c["sensible_heladas"]
            and estacion == "invierno"
            and "invierno" in c["estaciones"]
        ):
            advertencias.setdefault(nombre, []).append("ADV_HELADA")
        # R5.7 SUG_VERANO (estación verano + estaciones incluye verano)
        if estacion == "verano" and "verano" in c["estaciones"]:
            sugerencias.setdefault(nombre, []).append("SUG_VERANO")

    sin_resultados = len(recomendados) == 0

    return {
        "recomendados": sorted(recomendados),
        "descartes": descartes,
        "pautas": pautas,
        "sugerencias": sugerencias,
        "advertencias": advertencias,
        "sin_resultados": sin_resultados,
    }
