"""PASO 0: smoke test de Experta.

Confirma que:
  1. El parche de collections.Mapping se aplica antes de importar experta.
  2. Experta importa en esta versión de Python.
  3. Un KnowledgeEngine con una Rule trivial corre, dispara la regla y
     declara un nuevo hecho.

Si este script no termina con "[SMOKE TEST PASSED]", NO avanzar al PASO 1.
"""
import sys

# Parche obligatorio: Experta 1.9.4 falla al importar en Python >= 3.10
# porque usa collections.Mapping (movido a collections.abc en 3.10).
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

print(f"Python: {sys.version.splitlines()[0]}")

from experta import Fact, KnowledgeEngine, Rule  # noqa: E402

print("[OK] import experta")


class Entrada(Fact):
    pass


class Salida(Fact):
    pass


class MotorPrueba(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.disparadas: list[str] = []

    @Rule(Entrada(valor=42))
    def regla_trivial(self):
        self.disparadas.append("regla_trivial")
        self.declare(Salida(resultado="ok"))


motor = MotorPrueba()
motor.reset()
motor.declare(Entrada(valor=42))
motor.run()

assert motor.disparadas == ["regla_trivial"], f"La regla no disparó: {motor.disparadas}"
assert any(isinstance(f, Salida) for f in motor.facts.values()), \
    "Salida no fue declarada por la regla"

print("[OK] Regla trivial disparó y declaró el hecho de salida")
print("[SMOKE TEST PASSED]")
