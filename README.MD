# 🌱 Sistema Experto para Selección de Cultivos en Huertas Urbanas

Sistema experto basado en reglas diseñado para orientar a personas en entornos urbanos y domésticos (patios, balcones, terrazas o pequeños contenedores) en la elección de especies vegetales óptimas para cultivar según las condiciones agroecológicas y espaciales disponibles.

---

## 📌 Información del Trabajo

| Campo                     | Detalle                                                                                |
| :------------------------ | :------------------------------------------------------------------------------------- |
| **Universidad**           | Universidad de la Ciudad de Buenos Aires                                               |
| **Carrera**               | Licenciatura en Ciencia de Datos                                                       |
| **Materia**               | Análisis de Datos II: Sistemas Expertos y Redes de Conocimiento                        |
| **Trabajo**               | Trabajo Práctico Final - Sistema Experto para Selección de Cultivos en Huertas Urbanas |
| **Profesor**              | [Nombre del Profesor / Equipo Docente]                                                 |
| **Cuatrimestre**          | 2do Cuatrimestre 2026 (AD2_2026.2)                                                     |
| **Grupo Cliente**         | E                                                                                      |
| **Grupo Proveedor**       | F                                                                                      |
| **Fecha de Presentación** | [DD/MM/AAAA]                                                                           |

---

## 👥 Integrantes del Grupo

| Nombre y Apellido       |
| :---------------------- |
| Mauricio Chambi         |
| Daniel García           |
| Francisco Possamai      |
| Gabriela Pari Vaca      |
| Gabriela Martinez Soliz |

---

## 🌿 Descripción del Sistema

### 1. Resumen Ejecutivo

El sistema tiene como objetivo primordial brindar asesoramiento a personas que desean planificar o mantener una huerta en sus hogares (especialmente en departamentos o casas urbanas) y poseen conocimientos limitados o nulos en agricultura.

A través de una serie de preguntas simples, el usuario ingresa las condiciones reales de su entorno y el sistema evalúa su base de conocimientos mediante un motor de inferencia basado en reglas para determinar qué especies vegetales son viables, justificando cada recomendación de manera clara y accesible.

### 2. Dominio y Problema

- **Dominio:** Agricultura urbana agroecológica aplicada a patios, balcones, terrazas, canteros y macetas (con foco en la región del AMBA).
- **Definición del Problema:** _«Dadas las condiciones ambientales, espaciales y de disponibilidad de una huerta doméstica, determinar qué cultivos son adecuados para plantar y bajo qué recomendaciones de cuidado.»_
- **Justificación de la Solución:** La selección de cultivos responde a reglas determinísticas claras (tolerancia a la sombra/sol, estacionalidad, profundidad radicular y requerimientos de agua) catalogadas por entidades de investigación agronómica. No requiere un enfoque puramente estadístico o predictivo de caja negra, sino una lógica declarativa y transparente.

### 3. Entradas y Salidas del Sistema

#### Entradas (Condiciones solicitadas al usuario):

- ☀️ **Horas de luz solar directa:** Cantidad de heliofanía diaria disponible (sombra, semisombra o pleno sol).
- 📅 **Época del año / Estación:** Período de siembra (primavera-verano, otoño-invierno, anual).
- 📐 **Espacio y tipo de recipiente:** Balcón, terraza, cantero o suelo directo, junto con la profundidad/tamaño de las macetas.
- 💧 **Mantenimiento y disponibilidad de riego:** Frecuencia con la que el usuario puede realizar labores de cuidado e irrigación.

#### Salidas (Resultados ofrecidos al usuario):

- 🥗 **Cultivos recomendados:** Lista personalizada de especies aptas.
- 💡 **Explicación y Justificación:** Motivos agroecológicos que validan cada recomendación (ej. _«Apto para estación fría, requiere bajo volumen de suelo y tolera luz moderada»_).
- 🚰 **Pautas mínimas de cuidado:** Frecuencia sugerida de riego y recomendaciones de mantenimiento.
- 🚫 **Motivos de descarte (cuando aplique):** Factores limitantes por los cuales otras especies no resultaron aptas (ej. falta de profundidad de sustrato o insuficientes horas de sol).

### 4. Fuentes de Conocimiento

El motor de reglas se nutre y valida a partir de fuentes institucionales y bibliográficas de referencia:

- **INTA (Instituto Nacional de Tecnología Agropecuaria):** _Manual de la huerta agroecológica_.
- **INTA ProHuerta:** _Planificador de huerta_ y _Recomendaciones para especies básicas de huerta familiar urbana_.
