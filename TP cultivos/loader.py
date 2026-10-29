"""Carga del catálogo CSV.

Mapea los encabezados REALES del CSV v6 a los campos lógicos del motor.
Traduce strings a números y códigos. Rechaza cualquier valor desconocido
(riego, método, mes, booleano) con un ValueError claro: no filtra en silencio.
"""
from __future__ import annotations

import csv
from typing import Any


# ---------- Diccionarios de traducción ----------

MAPEO_RIEGO = {"bajo": 1, "moderado": 2, "frecuente": 3}

MAPEO_METODO = {
    "almacigo": "almacigo",
    "almácigo": "almacigo",
    "directa": "directa",
    "directo": "directa",
    "ambos": "ambos",
}

MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

ESTACIONES_COLS = ("verano", "otoño", "invierno", "primavera")

# Columnas que pasan al Fact Cultivo sin interpretar.
COLS_INFORMATIVAS = (
    "frecuencia_atencion_huerta",
    "labores_mantenimiento",
    "tipo_cosecha_manejo",
    "tipo_hortaliza",
    "días_cosecha",
    "fuente",
)


# ---------- Helpers ----------

def _s(valor: Any) -> str:
    """Normaliza un valor a str limpio, tratando None/NaN como ''."""
    if valor is None:
        return ""
    s = str(valor).strip()
    if s.lower() == "nan":
        return ""
    return s


def _parse_meses(valor: str, cultivo: str, columna: str) -> frozenset[int]:
    """Convierte el texto de meses del CSV a un frozenset de ints 1-12.

    Formatos aceptados:
      - "" (vacío)                     -> frozenset vacío
      - "todo_el_año"                  -> {1..12}
      - "septiembre"                   -> {9}
      - "octubre-noviembre"            -> {10, 11}
      - "diciembre-enero-marzo-mayo"   -> {12, 1, 3, 5}  (lista, no rango)

    Cualquier token que no sea un nombre de mes en español válido lanza
    ValueError con contexto (cultivo + columna).
    """
    s = _s(valor)
    if not s:
        return frozenset()
    if s == "todo_el_año":
        return frozenset(range(1, 13))

    tokens = [t.strip().lower() for t in s.split("-")]
    meses = []
    for tok in tokens:
        if tok not in MESES_ES:
            raise ValueError(
                f"[{cultivo}] columna '{columna}': mes desconocido "
                f"{tok!r} (valor completo: {valor!r})"
            )
        meses.append(MESES_ES[tok])
    return frozenset(meses)


def _parse_bool_sino(valor: str, cultivo: str, columna: str) -> bool:
    """'si' -> True, 'no' -> False; cualquier otra cosa -> ValueError."""
    s = _s(valor).lower()
    if s == "si":
        return True
    if s == "no":
        return False
    raise ValueError(
        f"[{cultivo}] columna '{columna}': se esperaba 'si' o 'no', "
        f"vino {valor!r}"
    )


def _parse_estacion(valor: str, cultivo: str, columna: str) -> bool:
    """TRUE/FALSE; case-insensitive. Cualquier otra cosa -> ValueError."""
    s = _s(valor).upper()
    if s == "TRUE":
        return True
    if s == "FALSE":
        return False
    raise ValueError(
        f"[{cultivo}] columna '{columna}': se esperaba 'TRUE' o 'FALSE', "
        f"vino {valor!r}"
    )


# ---------- Carga ----------

def cargar_cultivos(csv_path: str) -> list[dict]:
    """Devuelve una lista de diccionarios listos para instanciar Cultivo(**d).

    No depende de pandas: usa csv.DictReader (UTF-8). Las columnas tildadas
    del CSV (otoño, requiere_almácigo_protegido, días_cosecha) se leen tal cual.
    """
    out: list[dict] = []
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nombre = _s(row.get("cultivo"))
            if not nombre:
                raise ValueError("Fila sin nombre de cultivo en el CSV")

            # Riego: str -> int 1-3
            riego_str = _s(row.get("riego_nivel")).lower()
            if riego_str not in MAPEO_RIEGO:
                raise ValueError(
                    f"[{nombre}] columna 'riego_nivel': valor desconocido "
                    f"{riego_str!r} (válidos: {sorted(MAPEO_RIEGO)})"
                )
            riego_num = MAPEO_RIEGO[riego_str]

            # Método: normaliza tildes
            met_raw = _s(row.get("metodo_siembra")).lower()
            if met_raw not in MAPEO_METODO:
                raise ValueError(
                    f"[{nombre}] columna 'metodo_siembra': valor desconocido "
                    f"{met_raw!r} (válidos: {sorted(set(MAPEO_METODO))})"
                )
            metodo = MAPEO_METODO[met_raw]

            # Meses
            meses_siembra = _parse_meses(
                row.get("meses_siembra"), nombre, "meses_siembra"
            )
            meses_trasplante = _parse_meses(
                row.get("meses_trasplante"), nombre, "meses_trasplante"
            )

            # Estaciones (frozenset de strings TRUE)
            estaciones = []
            for col in ESTACIONES_COLS:
                if _parse_estacion(row.get(col), nombre, col):
                    estaciones.append(col)
            estaciones_fs = frozenset(estaciones)

            # Booleanos si/no
            sensible = _parse_bool_sino(
                row.get("sensible_a_heladas"), nombre, "sensible_a_heladas"
            )
            almacigo_prot = _parse_bool_sino(
                row.get("requiere_almácigo_protegido"),
                nombre,
                "requiere_almácigo_protegido",
            )

            # Numéricos
            try:
                horas_sol_min = float(row["horas_sol_min"])
                espacio_necesario_m2 = float(row["espacio_necesario_m_2"])
                profundidad_min_cm = float(row["profundidad_min_cm"])
            except (KeyError, ValueError) as e:
                raise ValueError(
                    f"[{nombre}] campo numérico inválido: {e}"
                ) from e

            out.append({
                "nombre": nombre,
                "horas_sol_min": horas_sol_min,
                "espacio_necesario_m2": espacio_necesario_m2,
                "profundidad_min_cm": profundidad_min_cm,
                "riego_num": riego_num,
                "meses_siembra": meses_siembra,
                "meses_trasplante": meses_trasplante,
                "estaciones": estaciones_fs,
                "sensible_heladas": sensible,
                "almacigo_protegido": almacigo_prot,
                "metodo_siembra": metodo,
                # Informativas (pasan sin interpretar)
                "frecuencia_atencion_huerta": _s(row.get("frecuencia_atencion_huerta")),
                "labores_mantenimiento": _s(row.get("labores_mantenimiento")),
                "tipo_cosecha_manejo": _s(row.get("tipo_cosecha_manejo")),
                "tipo_hortaliza": _s(row.get("tipo_hortaliza")),
                "dias_cosecha": _s(row.get("días_cosecha")),
                "fuente": _s(row.get("fuente")),
            })
    return out
