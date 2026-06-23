# 📈 ACME Stock Analytics

Sistema básico de análisis técnico de acciones con **pandas y NumPy**. Simula 60 días hábiles de precios para 3 perfiles de activo distintos y aplica indicadores estadísticos y técnicos clásicos para clasificar tendencia, volatilidad y generar señales de trading.

Proyecto desarrollado para análisis cuantitativo de series de tiempo financieras.

---

## 📋 Descripción

El script genera datos sintéticos de precios de cierre para 3 activos (ACME, VOLATIL, BAJISTA), cada uno con un perfil de rendimiento y volatilidad distinto, simulando 60 días hábiles de cotización. Después realiza:

- Estadísticas descriptivas por activo (precio actual, mínimo, máximo, promedio, mediana, desviación estándar)
- Cálculo de rendimientos diarios y rendimiento total compuesto
- Identificación del mejor y peor día, y conteo de días positivos/negativos
- Indicadores técnicos:
  - Media móvil simple (SMA)
  - Bandas de Bollinger
  - Máximos y mínimos locales
- Clasificación de tendencia (ALCISTA / BAJISTA / LATERAL) según precio vs media móvil
- Clasificación de volatilidad (BAJA / MEDIA / ALTA / MUY ALTA) según desviación estándar de rendimientos
- Generación de señales de trading (COMPRA / VENTA / MANTENER) mediante cruce de medias móviles
- Alertas de variaciones diarias superiores a un umbral definido
- Reporte comparativo entre los 3 activos + reporte detallado de ACME

---

## 📦 Requisitos

- Python 3.9+
- pandas
- NumPy

```bash
pip install pandas numpy