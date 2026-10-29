"""Clases Fact del motor Experta.

Separadas por nivel según secciones 0, A y C del Modelo_de_conocimiento_v6.pdf.
Ningún Fact lleva texto para el usuario: solo números y códigos.

El parche de collections.Mapping se aplica acá, ANTES de importar experta
(experta 1.9.4 fue publicado en 2019 y usa collections.Mapping, que en
Python >= 3.10 vive en collections.abc).
"""
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import Fact  # noqa: E402


# ---------- Nivel 0: entradas y dominio ----------

class DatosHuerta(Fact):
    """Entradas del usuario desde la UI.

    Campos:
      horas_sol (float 0-12), espacio_m2 (float >= 0),
      profundidad_cm (float > 0), mes (int 1-12), cuidado (int 1-3).
    """
    pass


class Cultivo(Fact):
    """Una especie del catálogo. Una instancia por fila del CSV."""
    pass


# ---------- Nivel 1: categorías y derivados ----------

class CategoriaLuz(Fact):
    """Discretización decorativa de horas de sol (R1.1a/b/c).

    Ninguna regla de descarte la lee: solo alimenta PerfilHuerta y es
    opcional en la UI.
    """
    pass


class CategoriaCuidado(Fact):
    """Código entero de cuidado 1-3 (R1.2)."""
    pass


class EstacionActual(Fact):
    """verano, otoño, invierno, primavera (R1.3a/b/c/d)."""
    pass


class CultivoEnVentana(Fact):
    """Dice que un cultivo tiene al mes actual en alguna de sus ventanas.

    Campos: cultivo (str), modo (siembra | ambas | plantines).
    Modos mutuamente excluyentes (R1.4a/b/c).
    """
    pass


# ---------- Nivel 2: perfil y temporada ----------

class PerfilHuerta(Fact):
    """Copia exacta de DatosHuerta más luz, cuidado y estacion ya resueltos.

    No discretiza horas_sol, espacio_m2, profundidad_cm ni mes.
    """
    pass


class CultivoEnTemporada(Fact):
    """Habilita las comparaciones numéricas de nivel 3 para un cultivo (R2.2)."""
    pass


# ---------- Nivel 3: evaluación numérica ----------

class Cumple(Fact):
    """Un criterio superado por el cultivo.

    Campos: cultivo, criterio (luz | espacio | recipiente | cuidado),
    codigo (plantilla), usr, req.
    """
    pass


class Falla(Fact):
    """Un criterio no superado. Mismos campos que Cumple."""
    pass


# ---------- Nivel 4: conclusiones ----------

class Recomendacion(Fact):
    """El cultivo cumple los cuatro criterios (R4.1)."""
    pass


class Descarte(Fact):
    """Un motivo de descarte. Un cultivo puede acumular varios.

    Campos: cultivo, motivo (epoca | luz | espacio | recipiente | cuidado),
    codigo. Para luz/espacio/recipiente/cuidado trae usr y req; para epoca
    trae mes, meses_siembra y meses_trasplante.
    """
    pass


class SinResultados(Fact):
    """Dispara cuando no quedó ninguna Recomendacion (R4.4)."""
    pass


# ---------- Nivel 5: enriquecimiento pedagógico ----------

class Pauta(Fact):
    """Pauta de riego, mantenimiento o cosecha (R5.1-R5.3).

    Campos: cultivo, tema (riego | mantenimiento | cosecha), codigo,
    y p1, p2, p3 con los datos informativos.
    """
    pass


class Sugerencia(Fact):
    """Sugerencia de inicio modo x metodo (R5.4) o consejo estacional (R5.7).

    Campos: cultivo, codigo.
    """
    pass


class Advertencia(Fact):
    """ADV_ALMACIGO (R5.5) o ADV_HELADA (R5.6).

    Campos: cultivo, codigo.
    """
    pass
