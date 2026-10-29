"""Config de pytest.

Agrega la raíz del proyecto a sys.path (vía su presencia aquí) para que
`tests/*` pueda importar los módulos de la raíz (facts, loader,
knowledge_base, textos, oraculo).

Define el flag `--run-slow`: el barrido completo de 9.000 combinaciones
del test_oraculo tarda varios minutos; por defecto queda skippeado. Para
correrlo: `pytest --run-slow`.
"""
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Corre los tests marcados @pytest.mark.slow (barrido 9000).",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: tests lentos (barrido 9.000). Correr con --run-slow.",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-slow"):
        return
    skip_slow = pytest.mark.skip(reason="necesita --run-slow")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
