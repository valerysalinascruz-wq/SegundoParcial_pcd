# 🌡️ MeteoSense Analytics

Sistema de análisis de datos meteorológicos con NumPy. Procesa mediciones simuladas de una red de 5 sensores en la Ciudad de México (temperatura, humedad relativa y CO2) durante 7 días, con lecturas cada hora.

Proyecto desarrollado para la materia *Programación para Ciencia de Datos*, IPN-ESCOM, 2026.

---

## 📋 Descripción

El script genera datos sintéticos de 5 estaciones de monitoreo (Coyoacán, Azcapotzalco, Xochimilco, Tlalpan, Miguel Hidalgo) y realiza un análisis completo usando exclusivamente operaciones vectorizadas de NumPy (sin loops for/while en el análisis), incluyendo:

- Exploración e inspección de arrays multidimensionales
- Indexación y slicing avanzado
- Estadísticas globales y por eje, con manejo de valores NaN
- Conversiones de unidades y cálculo de un Índice de Confort Térmico
- Detección de anomalías (criterio de ±2 desviaciones estándar)
- Análisis de impacto de un día de contingencia ambiental
- Reporte ejecutivo final con rankings y calidad de datos

## 📦 Requisitos

- Python 3.9+
- NumPy

bash
pip install numpy


## ▶️ Uso

1. Abre Jupyter Notebook / JupyterLab o Google Colab.
2. Pega el código en una celda (o en varias celdas siguiendo las secciones marcadas con ═══).
3. Ejecuta de principio a fin (Run All).

No requiere argumentos ni archivos externos: los datos se generan internamente con np.random.seed(42) para que los resultados sean reproducibles.

## 🗂️ Estructura de los datos

| Array | Shape | Descripción |
|---|---|---|
| temperatura | (5, 7, 24) | °C por estación, día, hora |
| humedad | (5, 7, 24) | % relativa por estación, día, hora |
| co2 | (5, 7, 24) | ppm por estación, día, hora |
| temp_promedio_diario | (5, 7) | Promedio diario por estación |
| humedad_promedio_diario | (5, 7) | Promedio diario por estación |
| co2_promedio_diario | (5, 7) | Promedio diario por estación |

Ejes del array 3D: axis=0 estaciones, axis=1 días, axis=2 horas.

Los arrays incluyen valores NaN simulando sensores desconectados; por eso todo el cálculo estadístico usa funciones nan* (nanmean, nanstd, nanmax, nanmin).

## 📊 Secciones del análisis

1. *Exploración de Arrays* — dimensiones, forma, tamaño, tipo de dato, memoria; indexación y slicing.
2. *Estadísticas Básicas* — estadísticas globales y por eje (por estación, por hora, por día).
3. *Operaciones Vectorizadas* — conversión °C→°F→K, normalización min-max, Índice de Confort Térmico (ICT = T + 0.05·H) y su clasificación (Frío / Confortable / Cálido / Muy caluroso).
4. *Análisis Avanzado* — detección de anomalías en CO2 y comparación del día de contingencia (día 4) contra días normales, identificando la estación más afectada.
5. *Reporte Ejecutivo (bonus)* — resumen con la estación más calurosa, más húmeda, con mejor calidad de aire, horas pico de temperatura/CO2 y conteo de valores faltantes.

## ✅ Notas

- Todo el código de análisis (partes 2 a 4) está vectorizado, sin loops explícitos.
- Reproducible: misma semilla (42) → mismos resultados siempre.
- Probado de inicio a fin sin errores.