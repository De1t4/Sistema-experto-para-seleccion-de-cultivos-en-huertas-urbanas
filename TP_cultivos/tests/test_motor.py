"""Validación del motor contra los 6 casos de prueba del PDF (sección D).

Para cada caso CP-01 a CP-06 verificamos EXACTAMENTE:
  - El conjunto de cultivos recomendados.
  - El conjunto de cultivos descartados, agrupado por motivo.
  - Si disparó o no SinResultados.
  - Las trazas de reglas (global y por cultivo), comparadas como conjunto.
    Experta no garantiza orden entre reglas de igual prioridad.
"""
from __future__ import annotations

import pytest

from loader import cargar_cultivos
from knowledge_base import ejecutar_motor


CSV = "data/cultivos_v6.csv"


@pytest.fixture(scope="module")
def catalogo():
    return cargar_cultivos(CSV)


# ---------- Casos de prueba (sección D del PDF) ----------

CASOS = {
    # ---------------- CP-01 ----------------
    "CP-01": {
        "entrada": dict(
            horas_sol=4.0, espacio_m2=0.5, profundidad_cm=25, mes=4, cuidado=2,
        ),
        "recomendados": {"Acelga", "Perejil"},
        "descartes_por_motivo": {
            "epoca": {
                "Albahaca", "Apio", "Calabaza", "Maíz dulce", "Melón",
                "Pepino", "Tomate", "Zapallito",
            },
            "cuidado": {"Espinaca", "Lechuga", "Rúcula"},
            "luz": {"Haba", "Rabanito", "Zanahoria"},
            "recipiente": {"Haba"},
        },
        "sin_resultados": False,
        "trazas": {
            "__global__": {"R1.1b", "R1.2", "R1.3b", "R2.1"},
            "Acelga": {
                "R1.4b", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4",
            },
            "Perejil": {
                "R1.4a", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4",
            },
            "Rúcula": {"R1.4a", "R2.2", "R3.1", "R3.3", "R3.5", "R3.8", "R4.2"},
            "Haba": {"R1.4a", "R2.2", "R3.2", "R3.3", "R3.6", "R3.7", "R4.2"},
            "Tomate": {"R4.3"},
        },
    },

    # ---------------- CP-02 ----------------
    "CP-02": {
        "entrada": dict(
            horas_sol=7.0, espacio_m2=4, profundidad_cm=45, mes=1, cuidado=3,
        ),
        "recomendados": {
            "Acelga", "Apio", "Calabaza", "Lechuga", "Rabanito",
            "Rúcula", "Zanahoria", "Zapallito",
        },
        "descartes_por_motivo": {
            "epoca": {
                "Albahaca", "Espinaca", "Haba", "Maíz dulce", "Melón",
                "Pepino", "Perejil", "Tomate",
            },
        },
        "sin_resultados": False,
        # Consejo de verano R5.7 se dispara en estos 6; NO en Apio ni Calabaza.
        "sugerencia_verano": {
            "Acelga", "Lechuga", "Rabanito", "Rúcula", "Zanahoria", "Zapallito",
        },
        "trazas": {
            "__global__": {"R1.1c", "R1.2", "R1.3a", "R2.1"},
            "Apio": {
                "R1.4c", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4",
            },
            "Acelga": {
                "R1.4b", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4", "R5.7",
            },
            "Rabanito": {
                "R1.4a", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4", "R5.7",
            },
        },
    },

    # ---------------- CP-03 ----------------
    "CP-03": {
        "entrada": dict(
            horas_sol=6.0, espacio_m2=2, profundidad_cm=40, mes=11, cuidado=3,
        ),
        "recomendados": {
            "Acelga", "Albahaca", "Apio", "Lechuga", "Maíz dulce",
            "Perejil", "Rabanito", "Rúcula", "Zanahoria", "Zapallito", "Tomate",
        },
        "descartes_por_motivo": {
            "espacio": {"Calabaza"},
            "epoca": {"Espinaca", "Haba", "Melón", "Pepino"},
        },
        "sin_resultados": False,
        # Tomate está en modo plantines => R5.5 NO aplica (sin ADV_ALMACIGO).
        "advertencias_tomate_vacio": True,
        "trazas": {
            "__global__": {"R1.1c", "R1.2", "R1.3d", "R2.1"},
            "Tomate": {
                "R1.4c", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4",
            },
            "Calabaza": {"R1.4a", "R2.2", "R3.1", "R3.4", "R3.5", "R3.7", "R4.2"},
            "Haba": {"R4.3"},
        },
    },

    # ---------------- CP-04 ----------------
    "CP-04": {
        "entrada": dict(
            horas_sol=2.0, espacio_m2=1, profundidad_cm=40, mes=7, cuidado=1,
        ),
        "recomendados": set(),
        "descartes_por_motivo": {
            # Luz y cuidado a la vez.
            "luz": {"Acelga", "Lechuga", "Rabanito", "Rúcula", "Tomate", "Zanahoria"},
            "cuidado": {"Acelga", "Lechuga", "Rabanito", "Rúcula", "Tomate", "Zanahoria"},
            "epoca": {
                "Albahaca", "Apio", "Calabaza", "Espinaca", "Haba",
                "Maíz dulce", "Melón", "Pepino", "Perejil", "Zapallito",
            },
        },
        "sin_resultados": True,
        "trazas": {
            "__global__": {"R1.1a", "R1.2", "R1.3c", "R2.1", "R4.4"},
            "Acelga": {"R1.4b", "R2.2", "R3.2", "R3.3", "R3.5", "R3.8", "R4.2"},
            "Rabanito": {"R1.4a", "R2.2", "R3.2", "R3.3", "R3.5", "R3.8", "R4.2"},
            "Haba": {"R4.3"},
        },
    },

    # ---------------- CP-05 ----------------
    "CP-05": {
        "entrada": dict(
            horas_sol=5.0, espacio_m2=2, profundidad_cm=40, mes=10, cuidado=3,
        ),
        "recomendados": {
            "Acelga", "Albahaca", "Apio", "Lechuga", "Maíz dulce",
            "Melón", "Pepino", "Perejil", "Rabanito", "Rúcula",
            "Zanahoria", "Zapallito",
        },
        "descartes_por_motivo": {
            "luz": {"Tomate"},        # 5.0 < 6
            "espacio": {"Calabaza"},  # 2 < 3.5
            "epoca": {"Espinaca", "Haba"},
        },
        "sin_resultados": False,
        "trazas": {
            "__global__": {"R1.1b", "R1.2", "R1.3d", "R2.1"},
            "Tomate": {"R1.4b", "R2.2", "R3.2", "R3.3", "R3.5", "R3.7", "R4.2"},
            "Calabaza": {"R1.4a", "R2.2", "R3.1", "R3.4", "R3.5", "R3.7", "R4.2"},
        },
    },

    # ---------------- CP-06 ----------------
    "CP-06": {
        "entrada": dict(
            horas_sol=6.0, espacio_m2=1, profundidad_cm=40, mes=7, cuidado=3,
        ),
        "recomendados": {
            "Acelga", "Lechuga", "Rabanito", "Rúcula", "Zanahoria", "Tomate",
        },
        "descartes_por_motivo": {
            "epoca": {
                "Albahaca", "Apio", "Calabaza", "Espinaca", "Haba",
                "Maíz dulce", "Melón", "Pepino", "Perejil", "Zapallito",
            },
        },
        "sin_resultados": False,
        # Tomate: ADV_HELADA (R5.6) y ADV_ALMACIGO (R5.5).
        "advertencias_tomate": {"ADV_HELADA", "ADV_ALMACIGO"},
        "trazas": {
            "__global__": {"R1.1c", "R1.2", "R1.3c", "R2.1"},
            "Tomate": {
                "R1.4a", "R2.2", "R3.1", "R3.3", "R3.5", "R3.7",
                "R4.1", "R5.1", "R5.2", "R5.3", "R5.4", "R5.5", "R5.6",
            },
        },
    },
}


# ---------- Helpers ----------

def _descartes_por_motivo(resultado):
    """Agrupa los Descarte emitidos por el motor en {motivo: set(cultivos)}."""
    out: dict[str, set[str]] = {}
    for d in resultado["descartes"]:
        out.setdefault(d["motivo"], set()).add(d["cultivo"])
    return out


# ---------- Tests parametrizados ----------

@pytest.mark.parametrize("caso_id", list(CASOS.keys()))
def test_recomendados(catalogo, caso_id):
    caso = CASOS[caso_id]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    assert set(r["recomendados"]) == caso["recomendados"], (
        f"[{caso_id}] recomendados divergen:\n"
        f"  obtenido: {sorted(r['recomendados'])}\n"
        f"  esperado: {sorted(caso['recomendados'])}"
    )


@pytest.mark.parametrize("caso_id", list(CASOS.keys()))
def test_descartes_por_motivo(catalogo, caso_id):
    caso = CASOS[caso_id]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    obtenido = _descartes_por_motivo(r)
    esperado = caso["descartes_por_motivo"]
    # Comparamos motivos presentes en el esperado uno a uno.
    assert set(obtenido.keys()) == set(esperado.keys()), (
        f"[{caso_id}] motivos de descarte divergen:\n"
        f"  obtenidos: {sorted(obtenido.keys())}\n"
        f"  esperados: {sorted(esperado.keys())}"
    )
    for motivo, esp in esperado.items():
        assert obtenido[motivo] == esp, (
            f"[{caso_id}] descartes por '{motivo}' divergen:\n"
            f"  obtenido: {sorted(obtenido[motivo])}\n"
            f"  esperado: {sorted(esp)}"
        )


@pytest.mark.parametrize("caso_id", list(CASOS.keys()))
def test_sin_resultados(catalogo, caso_id):
    caso = CASOS[caso_id]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    assert r["sin_resultados"] is caso["sin_resultados"], (
        f"[{caso_id}] SinResultados divergente: "
        f"obtenido={r['sin_resultados']} esperado={caso['sin_resultados']}"
    )


@pytest.mark.parametrize("caso_id", list(CASOS.keys()))
def test_traza_global(catalogo, caso_id):
    caso = CASOS[caso_id]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    esperado = caso["trazas"]["__global__"]
    assert r["traza_global"] == esperado, (
        f"[{caso_id}] traza global divergente:\n"
        f"  obtenida: {sorted(r['traza_global'])}\n"
        f"  esperada: {sorted(esperado)}"
    )


@pytest.mark.parametrize("caso_id", list(CASOS.keys()))
def test_trazas_por_cultivo(catalogo, caso_id):
    """Verifica los cultivos cuya traza el PDF detalla explícitamente."""
    caso = CASOS[caso_id]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    for cultivo, esperado in caso["trazas"].items():
        if cultivo == "__global__":
            continue
        obtenido = r["traza_por_cultivo"].get(cultivo, set())
        assert obtenido == esperado, (
            f"[{caso_id}] traza de '{cultivo}' divergente:\n"
            f"  obtenida: {sorted(obtenido)}\n"
            f"  esperada: {sorted(esperado)}"
        )


# ---------- Verificaciones específicas de nivel 5 ----------

def test_cp02_consejo_de_verano(catalogo):
    """Solo deben recibir SUG_VERANO los cultivos con columna verano=TRUE."""
    caso = CASOS["CP-02"]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    con_verano = {c for c, codigos in r["sugerencias"].items()
                  if "SUG_VERANO" in codigos}
    assert con_verano == caso["sugerencia_verano"], (
        f"CP-02 SUG_VERANO divergente:\n"
        f"  obtenido: {sorted(con_verano)}\n"
        f"  esperado: {sorted(caso['sugerencia_verano'])}"
    )


def test_cp03_tomate_sin_advertencias(catalogo):
    """Tomate en modo plantines no recibe ADV_ALMACIGO (R5.5 no aplica)."""
    caso = CASOS["CP-03"]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    adv_tomate = r["advertencias"].get("Tomate", [])
    assert adv_tomate == [], (
        f"CP-03 Tomate debería no tener advertencias, trajo {adv_tomate}"
    )


def test_cp06_tomate_dos_advertencias(catalogo):
    """CP-06 Tomate: ADV_HELADA (R5.6) y ADV_ALMACIGO (R5.5)."""
    caso = CASOS["CP-06"]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    assert set(r["advertencias"].get("Tomate", [])) == caso["advertencias_tomate"]


def test_cp06_tomate_sugerencia_inicio(catalogo):
    """CP-06 Tomate: modo siembra + metodo almacigo => SUG_SIEMBRA_ALMACIGO."""
    caso = CASOS["CP-06"]
    r = ejecutar_motor(catalogo, **caso["entrada"])
    sug = r["sugerencias"].get("Tomate", [])
    assert "SUG_SIEMBRA_ALMACIGO" in sug, (
        f"CP-06 Tomate debería tener SUG_SIEMBRA_ALMACIGO, trajo {sug}"
    )


# ---------- Loader: rechazos ----------

def test_loader_carga_16_cultivos():
    cultivos = cargar_cultivos(CSV)
    assert len(cultivos) == 16
    nombres = {c["nombre"] for c in cultivos}
    assert "Acelga" in nombres and "Tomate" in nombres and "Zapallito" in nombres


def test_loader_rechaza_riego_invalido(tmp_path):
    """El loader debe lanzar ValueError ante un valor desconocido de riego."""
    import csv as csvmod
    bad = tmp_path / "bad.csv"
    with open(CSV, encoding="utf-8") as src:
        rows = list(csvmod.DictReader(src))
    rows[0]["riego_nivel"] = "medio"  # valor inválido
    with open(bad, "w", encoding="utf-8", newline="") as dst:
        w = csvmod.DictWriter(dst, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    with pytest.raises(ValueError, match="riego_nivel"):
        cargar_cultivos(str(bad))
