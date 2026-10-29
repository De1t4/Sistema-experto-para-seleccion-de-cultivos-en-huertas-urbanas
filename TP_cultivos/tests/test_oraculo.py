"""Validación cruzada: motor Experta vs oráculo en Python puro.

Dos niveles de verificación:

  1. Fast (siempre): el oráculo debe coincidir con el motor en los 6 casos
     CP-01 a CP-06 del PDF (recomendados, descartes por motivo, nivel 5).
  2. Slow (opt-in con --run-slow): barrido completo de 9.000 combinaciones
     (12 meses × 3 cuidados × 10 valores de luz × 5 espacios × 5 profundidades),
     con las dos implementaciones corridas en paralelo y comparadas en
     cada caso. El PDF afirma que coinciden en los 9.000: este test lo
     verifica.
"""
from __future__ import annotations

import itertools

import pytest

from loader import cargar_cultivos
from knowledge_base import ejecutar_motor
from oraculo import ejecutar_oraculo


CSV = "data/cultivos_v6.csv"


# ---------- Fixtures ----------

@pytest.fixture(scope="module")
def catalogo():
    return cargar_cultivos(CSV)


# ---------- Normalización de outputs ----------

def _comparable(resultado: dict) -> dict:
    """Reduce el resultado a lo observable y comparable entre motor y oráculo.

    No compara trazas (el oráculo no es un motor de reglas) ni los p1/p2/p3
    de las Pautas (si el código PAU_* coincide, los textos del CSV son los
    mismos). Compara:
      - set de recomendados
      - set de (cultivo, motivo) para descartes
      - set de (cultivo, codigo_pauta) para pautas
      - set de (cultivo, codigo) para sugerencias y advertencias
      - sin_resultados (bool)
    """
    descartes_set = frozenset(
        (d["cultivo"], d["motivo"]) for d in resultado["descartes"]
    )
    pautas_set = frozenset(
        (cultivo, p["codigo"])
        for cultivo, lista in resultado["pautas"].items()
        for p in lista
    )
    sugerencias_set = frozenset(
        (cultivo, codigo)
        for cultivo, codigos in resultado["sugerencias"].items()
        for codigo in codigos
    )
    advertencias_set = frozenset(
        (cultivo, codigo)
        for cultivo, codigos in resultado["advertencias"].items()
        for codigo in codigos
    )
    return {
        "recomendados": frozenset(resultado["recomendados"]),
        "descartes": descartes_set,
        "pautas": pautas_set,
        "sugerencias": sugerencias_set,
        "advertencias": advertencias_set,
        "sin_resultados": resultado["sin_resultados"],
    }


def _diff(motor_cmp: dict, oraculo_cmp: dict) -> str:
    """Devuelve un string con la diferencia campo por campo."""
    partes = []
    for k in motor_cmp:
        if motor_cmp[k] != oraculo_cmp[k]:
            partes.append(
                f"  {k}:\n"
                f"    motor:    {sorted(motor_cmp[k]) if isinstance(motor_cmp[k], frozenset) else motor_cmp[k]}\n"
                f"    oraculo:  {sorted(oraculo_cmp[k]) if isinstance(oraculo_cmp[k], frozenset) else oraculo_cmp[k]}\n"
                f"    solo motor:  {sorted(motor_cmp[k] - oraculo_cmp[k]) if isinstance(motor_cmp[k], frozenset) else '-'}\n"
                f"    solo oracle: {sorted(oraculo_cmp[k] - motor_cmp[k]) if isinstance(motor_cmp[k], frozenset) else '-'}"
            )
    return "\n".join(partes) if partes else "(sin diferencias)"


# ---------- Fast: 6 CP ----------

CP_ENTRADAS = {
    "CP-01": dict(horas_sol=4.0, espacio_m2=0.5, profundidad_cm=25, mes=4, cuidado=2),
    "CP-02": dict(horas_sol=7.0, espacio_m2=4, profundidad_cm=45, mes=1, cuidado=3),
    "CP-03": dict(horas_sol=6.0, espacio_m2=2, profundidad_cm=40, mes=11, cuidado=3),
    "CP-04": dict(horas_sol=2.0, espacio_m2=1, profundidad_cm=40, mes=7, cuidado=1),
    "CP-05": dict(horas_sol=5.0, espacio_m2=2, profundidad_cm=40, mes=10, cuidado=3),
    "CP-06": dict(horas_sol=6.0, espacio_m2=1, profundidad_cm=40, mes=7, cuidado=3),
}


@pytest.mark.parametrize("caso_id", list(CP_ENTRADAS.keys()))
def test_oraculo_coincide_con_motor_en_cp(catalogo, caso_id):
    """En los 6 casos del PDF el oráculo debe dar lo mismo que el motor."""
    entrada = CP_ENTRADAS[caso_id]
    r_motor = _comparable(ejecutar_motor(catalogo, **entrada))
    r_oraculo = _comparable(ejecutar_oraculo(catalogo, **entrada))
    assert r_motor == r_oraculo, (
        f"[{caso_id}] motor y oráculo divergen:\n{_diff(r_motor, r_oraculo)}"
    )


# ---------- Fast: muestra chica del barrido (sanity) ----------

VALORES_LUZ = [0.0, 2.0, 3.0, 4.0, 5.0, 5.5, 6.0, 7.0, 8.0, 10.0]
VALORES_ESPACIO = [0.05, 0.3, 1.0, 2.0, 4.0]
VALORES_PROFUNDIDAD = [10.0, 25.0, 30.0, 40.0, 50.0]
MESES = list(range(1, 13))
CUIDADOS = [1, 2, 3]


def _combinaciones():
    """Las 9.000 combinaciones del barrido del PDF."""
    for mes, cuidado, horas, esp, prof in itertools.product(
        MESES, CUIDADOS, VALORES_LUZ, VALORES_ESPACIO, VALORES_PROFUNDIDAD,
    ):
        yield mes, cuidado, horas, esp, prof


def test_barrido_tiene_9000_combinaciones():
    """La geometría del barrido es exactamente la del PDF."""
    assert sum(1 for _ in _combinaciones()) == 9000


def test_oraculo_muestra_sanity(catalogo):
    """Muestra chica del barrido: 1 de cada 100 combinaciones.

    No reemplaza al barrido completo, pero es un smoke rápido que corre en
    pytest default. El barrido completo vive detrás de --run-slow.
    """
    discrepancias = []
    for i, (mes, cuidado, horas, esp, prof) in enumerate(_combinaciones()):
        if i % 100 != 0:
            continue
        r_m = _comparable(ejecutar_motor(catalogo, horas, esp, prof, mes, cuidado))
        r_o = _comparable(ejecutar_oraculo(catalogo, horas, esp, prof, mes, cuidado))
        if r_m != r_o:
            discrepancias.append((mes, cuidado, horas, esp, prof))
            if len(discrepancias) >= 3:
                break
    assert not discrepancias, (
        f"Muestra con discrepancias: {discrepancias}"
    )


# ---------- Slow: barrido completo de 9.000 ----------

@pytest.mark.slow
def test_oraculo_barrido_completo_9000(catalogo):
    """Verifica que motor Experta y oráculo coinciden en las 9.000 combinaciones.

    Reproduce exactamente la afirmación del PDF (sección 0): "un oráculo
    independiente en Python puro y el motor Experta dan el mismo resultado
    en las 9.000 combinaciones de un barrido sobre cultivos_v6.csv".

    Corre con: pytest --run-slow
    Dura unos minutos (~70 ms por run del motor Experta).
    """
    discrepancias = []
    total = 0
    for mes, cuidado, horas, esp, prof in _combinaciones():
        total += 1
        r_m = _comparable(ejecutar_motor(catalogo, horas, esp, prof, mes, cuidado))
        r_o = _comparable(ejecutar_oraculo(catalogo, horas, esp, prof, mes, cuidado))
        if r_m != r_o:
            discrepancias.append({
                "entrada": dict(
                    mes=mes, cuidado=cuidado, horas_sol=horas,
                    espacio_m2=esp, profundidad_cm=prof,
                ),
                "diff": _diff(r_m, r_o),
            })
            if len(discrepancias) >= 3:
                break
    assert total == 9000, f"Esperaba 9000 combinaciones, hubo {total}"
    assert not discrepancias, (
        f"Discrepancias motor vs oráculo en {len(discrepancias)} de 9000:\n"
        + "\n---\n".join(
            f"entrada {d['entrada']}:\n{d['diff']}" for d in discrepancias
        )
    )
