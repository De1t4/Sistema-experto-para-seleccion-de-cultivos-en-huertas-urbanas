"""Motor Experta: 25 reglas lógicas distribuidas en 32 @Rule, en 5 niveles.

Implementación literal del PDF Modelo_de_conocimiento_v6, secciones C.1 a C.5.
Este archivo solo trabaja con números y códigos: ningún texto para el usuario.
El rendering de códigos vive en textos.py.
"""
from __future__ import annotations

# Parche de collections.Mapping. facts.py también lo aplica, pero lo dejamos
# acá explícito para no depender del orden de imports.
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, MATCH, TEST, NOT  # noqa: E402

from facts import (  # noqa: E402
    DatosHuerta, Cultivo, CategoriaLuz, CategoriaCuidado, EstacionActual,
    CultivoEnVentana, PerfilHuerta, CultivoEnTemporada,
    Cumple, Falla, Recomendacion, Descarte, SinResultados,
    Pauta, Sugerencia, Advertencia,
)
from textos import CODIGO_INICIO  # noqa: E402  (tabla de códigos, no texto UI)


GLOBAL = "__global__"  # clave convencional para la traza sin cultivo


class Motor(KnowledgeEngine):
    """Motor Experta con las 32 @Rule del modelo.

    Guarda la traza de reglas disparadas en:
      - self.traza_global: set[str]  (reglas sin cultivo asociado)
      - self.traza_por_cultivo: dict[str, set[str]]  (reglas por cultivo)
    """

    def __init__(self):
        super().__init__()
        self.traza_global: set[str] = set()
        self.traza_por_cultivo: dict[str, set[str]] = {}

    def reset(self, **kwargs):
        super().reset(**kwargs)
        self.traza_global = set()
        self.traza_por_cultivo = {}

    def _log(self, regla: str, cultivo: str | None = None) -> None:
        if cultivo is None:
            self.traza_global.add(regla)
        else:
            self.traza_por_cultivo.setdefault(cultivo, set()).add(regla)

    # ================================================================
    # Nivel 1 — categorías y derivados (4 reglas lógicas, 11 @Rule)
    # ================================================================

    # ---- R1.1 Luz decorativa (3 @Rule) ----
    @Rule(DatosHuerta(horas_sol=MATCH.h), TEST(lambda h: h < 3))
    def r1_1a(self, h):
        self._log("R1.1a")
        self.declare(CategoriaLuz(nivel="baja"))

    @Rule(DatosHuerta(horas_sol=MATCH.h), TEST(lambda h: 3 <= h <= 5))
    def r1_1b(self, h):
        self._log("R1.1b")
        self.declare(CategoriaLuz(nivel="media"))

    @Rule(DatosHuerta(horas_sol=MATCH.h), TEST(lambda h: h > 5))
    def r1_1c(self, h):
        self._log("R1.1c")
        self.declare(CategoriaLuz(nivel="alta"))

    # ---- R1.2 Cuidado 1-3 (1 @Rule) ----
    @Rule(DatosHuerta(cuidado=MATCH.u), TEST(lambda u: u in (1, 2, 3)))
    def r1_2(self, u):
        self._log("R1.2")
        self.declare(CategoriaCuidado(nivel=u))

    # ---- R1.3 Estación (4 @Rule) ----
    @Rule(DatosHuerta(mes=MATCH.m), TEST(lambda m: m in (12, 1, 2)))
    def r1_3a(self, m):
        self._log("R1.3a")
        self.declare(EstacionActual(nombre="verano"))

    @Rule(DatosHuerta(mes=MATCH.m), TEST(lambda m: m in (3, 4, 5)))
    def r1_3b(self, m):
        self._log("R1.3b")
        self.declare(EstacionActual(nombre="otoño"))

    @Rule(DatosHuerta(mes=MATCH.m), TEST(lambda m: m in (6, 7, 8)))
    def r1_3c(self, m):
        self._log("R1.3c")
        self.declare(EstacionActual(nombre="invierno"))

    @Rule(DatosHuerta(mes=MATCH.m), TEST(lambda m: m in (9, 10, 11)))
    def r1_3d(self, m):
        self._log("R1.3d")
        self.declare(EstacionActual(nombre="primavera"))

    # ---- R1.4 Modo de vigencia (3 @Rule, mutuamente excluyentes) ----
    @Rule(
        DatosHuerta(mes=MATCH.m),
        Cultivo(nombre=MATCH.c, meses_siembra=MATCH.ms, meses_trasplante=MATCH.mt),
        TEST(lambda m, ms, mt: m in ms and m not in mt),
    )
    def r1_4a(self, c, m, ms, mt):
        self._log("R1.4a", c)
        self.declare(CultivoEnVentana(cultivo=c, modo="siembra"))

    @Rule(
        DatosHuerta(mes=MATCH.m),
        Cultivo(nombre=MATCH.c, meses_siembra=MATCH.ms, meses_trasplante=MATCH.mt),
        TEST(lambda m, ms, mt: m in ms and m in mt),
    )
    def r1_4b(self, c, m, ms, mt):
        self._log("R1.4b", c)
        self.declare(CultivoEnVentana(cultivo=c, modo="ambas"))

    @Rule(
        DatosHuerta(mes=MATCH.m),
        Cultivo(nombre=MATCH.c, meses_siembra=MATCH.ms, meses_trasplante=MATCH.mt),
        TEST(lambda m, ms, mt: m not in ms and m in mt),
    )
    def r1_4c(self, c, m, ms, mt):
        self._log("R1.4c", c)
        self.declare(CultivoEnVentana(cultivo=c, modo="plantines"))

    # ================================================================
    # Nivel 2 — perfil y temporada (2 reglas, 2 @Rule)
    # ================================================================

    @Rule(
        DatosHuerta(
            horas_sol=MATCH.h,
            espacio_m2=MATCH.e,
            profundidad_cm=MATCH.p,
            mes=MATCH.m,
        ),
        CategoriaLuz(nivel=MATCH.l),
        CategoriaCuidado(nivel=MATCH.u),
        EstacionActual(nombre=MATCH.s),
    )
    def r2_1(self, h, e, p, m, l, u, s):
        self._log("R2.1")
        self.declare(PerfilHuerta(
            horas_sol=h, espacio_m2=e, profundidad_cm=p, mes=m,
            luz=l, cuidado=u, estacion=s,
        ))

    @Rule(CultivoEnVentana(cultivo=MATCH.c))
    def r2_2(self, c):
        self._log("R2.2", c)
        self.declare(CultivoEnTemporada(cultivo=c))

    # ================================================================
    # Nivel 3 — comparación numérica (8 reglas, 8 @Rule)
    # Todas exigen CultivoEnTemporada(c). Comparación estricta en luz.
    # ================================================================

    # ---- R3.1 / R3.2 Luz ----
    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(horas_sol=MATCH.h_usr),
        Cultivo(nombre=MATCH.c, horas_sol_min=MATCH.h_min),
        TEST(lambda h_usr, h_min: h_usr >= h_min),
    )
    def r3_1(self, c, h_usr, h_min):
        self._log("R3.1", c)
        self.declare(Cumple(
            cultivo=c, criterio="luz", codigo="LUZ_OK", usr=h_usr, req=h_min,
        ))

    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(horas_sol=MATCH.h_usr),
        Cultivo(nombre=MATCH.c, horas_sol_min=MATCH.h_min),
        TEST(lambda h_usr, h_min: h_usr < h_min),
    )
    def r3_2(self, c, h_usr, h_min):
        self._log("R3.2", c)
        self.declare(Falla(
            cultivo=c, criterio="luz", codigo="LUZ_FALTA", usr=h_usr, req=h_min,
        ))

    # ---- R3.3 / R3.4 Espacio ----
    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(espacio_m2=MATCH.e_usr),
        Cultivo(nombre=MATCH.c, espacio_necesario_m2=MATCH.e_min),
        TEST(lambda e_usr, e_min: e_usr >= e_min),
    )
    def r3_3(self, c, e_usr, e_min):
        self._log("R3.3", c)
        self.declare(Cumple(
            cultivo=c, criterio="espacio", codigo="ESP_OK", usr=e_usr, req=e_min,
        ))

    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(espacio_m2=MATCH.e_usr),
        Cultivo(nombre=MATCH.c, espacio_necesario_m2=MATCH.e_min),
        TEST(lambda e_usr, e_min: e_usr < e_min),
    )
    def r3_4(self, c, e_usr, e_min):
        self._log("R3.4", c)
        self.declare(Falla(
            cultivo=c, criterio="espacio", codigo="ESP_FALTA", usr=e_usr, req=e_min,
        ))

    # ---- R3.5 / R3.6 Recipiente ----
    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(profundidad_cm=MATCH.p_usr),
        Cultivo(nombre=MATCH.c, profundidad_min_cm=MATCH.p_min),
        TEST(lambda p_usr, p_min: p_usr >= p_min),
    )
    def r3_5(self, c, p_usr, p_min):
        self._log("R3.5", c)
        self.declare(Cumple(
            cultivo=c, criterio="recipiente", codigo="REC_OK", usr=p_usr, req=p_min,
        ))

    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(profundidad_cm=MATCH.p_usr),
        Cultivo(nombre=MATCH.c, profundidad_min_cm=MATCH.p_min),
        TEST(lambda p_usr, p_min: p_usr < p_min),
    )
    def r3_6(self, c, p_usr, p_min):
        self._log("R3.6", c)
        self.declare(Falla(
            cultivo=c, criterio="recipiente", codigo="REC_FALTA", usr=p_usr, req=p_min,
        ))

    # ---- R3.7 / R3.8 Cuidado ----
    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(cuidado=MATCH.u_usr),
        Cultivo(nombre=MATCH.c, riego_num=MATCH.r_min),
        TEST(lambda u_usr, r_min: u_usr >= r_min),
    )
    def r3_7(self, c, u_usr, r_min):
        self._log("R3.7", c)
        self.declare(Cumple(
            cultivo=c, criterio="cuidado", codigo="CUI_OK", usr=u_usr, req=r_min,
        ))

    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        PerfilHuerta(cuidado=MATCH.u_usr),
        Cultivo(nombre=MATCH.c, riego_num=MATCH.r_min),
        TEST(lambda u_usr, r_min: u_usr < r_min),
    )
    def r3_8(self, c, u_usr, r_min):
        self._log("R3.8", c)
        self.declare(Falla(
            cultivo=c, criterio="cuidado", codigo="CUI_FALTA", usr=u_usr, req=r_min,
        ))

    # ================================================================
    # Nivel 4 — conclusiones (4 reglas, 4 @Rule)
    # R4.3 (-10) y R4.4 (-20) razonan por ausencia: corren DESPUÉS.
    # ================================================================

    @Rule(
        CultivoEnTemporada(cultivo=MATCH.c),
        Cumple(cultivo=MATCH.c, criterio="luz"),
        Cumple(cultivo=MATCH.c, criterio="espacio"),
        Cumple(cultivo=MATCH.c, criterio="recipiente"),
        Cumple(cultivo=MATCH.c, criterio="cuidado"),
    )
    def r4_1(self, c):
        self._log("R4.1", c)
        self.declare(Recomendacion(cultivo=c))

    @Rule(Falla(
        cultivo=MATCH.c, criterio=MATCH.k, codigo=MATCH.cod,
        usr=MATCH.u, req=MATCH.r,
    ))
    def r4_2(self, c, k, cod, u, r):
        self._log("R4.2", c)
        self.declare(Descarte(
            cultivo=c, motivo=k, codigo=cod, usr=u, req=r,
        ))

    @Rule(
        Cultivo(nombre=MATCH.c, meses_siembra=MATCH.ms, meses_trasplante=MATCH.mt),
        PerfilHuerta(mes=MATCH.m),
        NOT(CultivoEnTemporada(cultivo=MATCH.c)),
        salience=-10,
    )
    def r4_3(self, c, m, ms, mt):
        self._log("R4.3", c)
        self.declare(Descarte(
            cultivo=c, motivo="epoca", codigo="DESC_EPOCA",
            mes=m, meses_siembra=ms, meses_trasplante=mt,
        ))

    @Rule(
        PerfilHuerta(),
        NOT(Recomendacion()),
        salience=-20,
    )
    def r4_4(self):
        self._log("R4.4")
        self.declare(SinResultados(codigo="MSG_SIN_RESULTADOS"))

    # ================================================================
    # Nivel 5 — enriquecimiento pedagógico (7 reglas, 7 @Rule)
    # Solo para cultivos recomendados.
    # ================================================================

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(nombre=MATCH.c, riego_num=MATCH.rn),
    )
    def r5_1(self, c, rn):
        self._log("R5.1", c)
        self.declare(Pauta(
            cultivo=c, tema="riego", codigo=f"PAU_RIEGO_{rn}",
        ))

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(
            nombre=MATCH.c,
            labores_mantenimiento=MATCH.lm,
            frecuencia_atencion_huerta=MATCH.fa,
        ),
    )
    def r5_2(self, c, lm, fa):
        self._log("R5.2", c)
        self.declare(Pauta(
            cultivo=c, tema="mantenimiento", codigo="PAU_MANT",
            p1=lm, p2=fa,
        ))

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(
            nombre=MATCH.c,
            tipo_cosecha_manejo=MATCH.tcm,
            dias_cosecha=MATCH.dc,
            tipo_hortaliza=MATCH.th,
        ),
    )
    def r5_3(self, c, tcm, dc, th):
        self._log("R5.3", c)
        self.declare(Pauta(
            cultivo=c, tema="cosecha", codigo="PAU_COS",
            p1=tcm, p2=dc, p3=th,
        ))

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(nombre=MATCH.c, metodo_siembra=MATCH.met),
        CultivoEnVentana(cultivo=MATCH.c, modo=MATCH.modo),
    )
    def r5_4(self, c, met, modo):
        self._log("R5.4", c)
        codigo = CODIGO_INICIO[(modo, met)]
        self.declare(Sugerencia(cultivo=c, codigo=codigo))

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(nombre=MATCH.c, almacigo_protegido=True),
        CultivoEnVentana(cultivo=MATCH.c, modo=MATCH.modo),
        TEST(lambda modo: modo != "plantines"),
    )
    def r5_5(self, c):
        self._log("R5.5", c)
        self.declare(Advertencia(cultivo=c, codigo="ADV_ALMACIGO"))

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(nombre=MATCH.c, sensible_heladas=True, estaciones=MATCH.ests),
        PerfilHuerta(estacion="invierno"),
        TEST(lambda ests: "invierno" in ests),
    )
    def r5_6(self, c):
        self._log("R5.6", c)
        self.declare(Advertencia(cultivo=c, codigo="ADV_HELADA"))

    @Rule(
        Recomendacion(cultivo=MATCH.c),
        Cultivo(nombre=MATCH.c, estaciones=MATCH.ests),
        PerfilHuerta(estacion="verano"),
        TEST(lambda ests: "verano" in ests),
    )
    def r5_7(self, c):
        self._log("R5.7", c)
        self.declare(Sugerencia(cultivo=c, codigo="SUG_VERANO"))


# ================================================================
# API pública: ejecutar_motor
# ================================================================

def ejecutar_motor(
    cultivos: list[dict],
    horas_sol: float,
    espacio_m2: float,
    profundidad_cm: float,
    mes: int,
    cuidado: int,
) -> dict:
    """Corre el motor con los datos del usuario y devuelve el resultado.

    Devuelve un dict con:
      - recomendados:   list[str]  (nombres de cultivos recomendados)
      - descartes:      list[dict] (uno por hecho Descarte, con todos sus campos)
      - pautas:         dict[str, list[dict]]  (cultivo -> [pautas])
      - sugerencias:    dict[str, list[str]]   (cultivo -> [codigos])
      - advertencias:   dict[str, list[str]]   (cultivo -> [codigos])
      - sin_resultados: bool
      - traza_global:   set[str]
      - traza_por_cultivo: dict[str, set[str]]
    """
    motor = Motor()
    motor.reset()
    motor.declare(DatosHuerta(
        horas_sol=float(horas_sol),
        espacio_m2=float(espacio_m2),
        profundidad_cm=float(profundidad_cm),
        mes=int(mes),
        cuidado=int(cuidado),
    ))
    for c in cultivos:
        motor.declare(Cultivo(**c))
    motor.run()

    recomendados: list[str] = []
    descartes: list[dict] = []
    pautas: dict[str, list[dict]] = {}
    sugerencias: dict[str, list[str]] = {}
    advertencias: dict[str, list[str]] = {}
    sin_resultados = False

    for f in motor.facts.values():
        if isinstance(f, Recomendacion):
            recomendados.append(f["cultivo"])
        elif isinstance(f, Descarte):
            # Expandir todos los campos del hecho.
            descartes.append({k: f[k] for k in f.keys() if not str(k).startswith("__")})
        elif isinstance(f, Pauta):
            d = {k: f[k] for k in f.keys() if not str(k).startswith("__")}
            pautas.setdefault(d["cultivo"], []).append(d)
        elif isinstance(f, Sugerencia):
            sugerencias.setdefault(f["cultivo"], []).append(f["codigo"])
        elif isinstance(f, Advertencia):
            advertencias.setdefault(f["cultivo"], []).append(f["codigo"])
        elif isinstance(f, SinResultados):
            sin_resultados = True

    return {
        "recomendados": sorted(recomendados),
        "descartes": descartes,
        "pautas": pautas,
        "sugerencias": sugerencias,
        "advertencias": advertencias,
        "sin_resultados": sin_resultados,
        "traza_global": motor.traza_global,
        "traza_por_cultivo": motor.traza_por_cultivo,
    }
