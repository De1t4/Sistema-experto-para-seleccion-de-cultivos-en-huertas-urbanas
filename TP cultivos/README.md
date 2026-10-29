# Selector de cultivos — huerta urbana (AMBA)

Sistema experto en Streamlit para elegir cultivos para una huerta urbana del
AMBA. Toma los datos de la huerta del usuario (horas de sol, espacio,
profundidad del recipiente, mes y nivel de riego posible) y devuelve
cultivos recomendados, con pautas de riego, mantenimiento y cosecha,
sugerencias de inicio y advertencias; además lista los descartados y el
motivo.

Proyecto académico de Análisis de Datos II (2026.2). Catálogo:
`data/cultivos_v6.csv` (16 especies). Motor: [Experta](https://pypi.org/project/experta/) 1.9.4,
encadenamiento hacia adelante, 25 reglas lógicas distribuidas en 32 `@Rule`
en 5 niveles. La especificación completa está en
`Modelo_de_conocimiento_v6.pdf`.

## Estructura

```
TP cultivos/
├── app.py                 # UI Streamlit (archivo principal del deploy)
├── knowledge_base.py      # Motor Experta: 32 @Rule en 5 niveles
├── facts.py               # Subclases de experta.Fact + parche de collections.Mapping
├── loader.py              # Lee el CSV, traduce a números y códigos
├── textos.py              # Plantillas C.6, tabla C.7, aviso fijo
├── oraculo.py             # Segunda implementación en Python puro (sin Experta)
├── smoke_test.py          # PASO 0: valida que Experta importa y corre
├── requirements.txt       # Versiones fijas
├── .python-version        # Python 3.11 para Streamlit Community Cloud
├── data/
│   └── cultivos_v6.csv    # Catálogo de 16 especies
├── tests/
│   ├── test_motor.py      # Casos CP-01 a CP-06 del PDF (36 tests)
│   └── test_oraculo.py    # Motor vs oráculo: 6 CP + muestra + barrido 9000
└── conftest.py            # Agrega raíz al sys.path y define --run-slow
```

## Correr localmente (Windows / Python 3.11)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python smoke_test.py
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\streamlit run app.py
```

En macOS / Linux reemplazá `py -3.11` por `python3.11` y
`.\.venv\Scripts\` por `.venv/bin/`.

## Deploy en Streamlit Community Cloud

1. Subí el repo a GitHub.
2. En [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Elegí el repo, la rama y `app.py` como archivo principal.
4. En **Advanced settings** confirmá Python 3.11 (lo pide `.python-version`).
5. Deploy.

Streamlit Cloud instala las dependencias desde `requirements.txt`. El pin
`experta==1.9.4` + `frozendict==1.2` es rígido y necesita Python 3.11 para
compilar `frozendict` desde fuente; por eso dejamos `.python-version`.

## Validación

Dos niveles de verificación:

**1. Casos del PDF (siempre).** La sección D del PDF trae seis casos de
prueba (CP-01 a CP-06) con sus resultados exactos: recomendados,
descartes por motivo y trazas de reglas. `tests/test_motor.py` corre esos
seis casos y falla si algo no coincide. Las trazas se comparan como
conjunto porque Experta no garantiza orden entre reglas de igual
prioridad.

**2. Oráculo independiente (opt-in).** `oraculo.py` es una segunda
implementación de las mismas 25 reglas lógicas, hecha en Python puro
(solo `if`/`for`, sin motor de reglas). `tests/test_oraculo.py` compara
motor Experta contra oráculo en los 6 CP (siempre) y, con
`--run-slow`, en el barrido completo de **9.000 combinaciones**
(12 meses × 3 cuidados × 10 valores de luz × 5 espacios × 5 profundidades)
que menciona el PDF en la sección 0. Las 9.000 coinciden exactamente
(verificado en 6:05 min).

```powershell
# Rápido: 44 tests, ~5 s
.\.venv\Scripts\python -m pytest -v

# Completo: suma el barrido de 9.000, ~6 min
.\.venv\Scripts\python -m pytest -v --run-slow
```

## Para la defensa

- Las tres `@Rule` R1.1 solo discretizan la luz para mostrarla en la UI:
  son decorativas y no participan de ningún descarte.
- R4.3 (`salience=-10`) y R4.4 (`salience=-20`) razonan por **ausencia**
  de hechos. La salience negativa garantiza que corran DESPUÉS de todas
  las reglas de prioridad 0.
- La vigencia (modo siembra / ambas / plantines / ninguno) depende SOLO
  de `meses_siembra` y `meses_trasplante`. Las columnas de estación del
  CSV no deciden vigencia; solo condicionan los consejos de nivel 5
  (R5.6 ADV_HELADA, R5.7 SUG_VERANO).
- Los mensajes para el usuario salen únicamente de las plantillas de C.6
  (`textos.PLANTILLAS`), indexados por código. El motor nunca manipula
  texto de usuario.
- El oráculo (`oraculo.py`) no es solo un chequeo: también sirve de
  **Plan B de deploy**. Si Streamlit Community Cloud rompe la
  compatibilidad con `experta==1.9.4` (depende de `frozendict==1.2`,
  2017), basta cambiar una línea en `app.py` para que la UI consuma
  `ejecutar_oraculo` en lugar de `ejecutar_motor`.
