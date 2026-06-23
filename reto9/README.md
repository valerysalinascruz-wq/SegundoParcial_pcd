# 🔍 SecureBank Fraud Detection

Sistema básico de detección de transacciones anómalas con NumPy. Simula 500 transacciones por cada una de 5 categorías de comercio y aplica dos métodos estadísticos clásicos (IQR y Z-Score) para identificar posibles fraudes.

Proyecto desarrollado para la materia **Programación para Ciencia de Datos**, IPN-ESCOM, 2026.

---

## 📋 Descripción

El script genera datos sintéticos de transacciones bancarias para 5 categorías de comercio (Supermercados, Restaurantes, Gasolineras, Tiendas Online, Entretenimiento), inyectando entre 3% y 5% de anomalías (montos sospechosamente altos o bajos) por categoría. Después realiza:

- Estadísticas descriptivas por categoría (media, mediana, desviación estándar, mínimo, máximo)
- Cálculo de cuartiles (Q1, Q2, Q3) y rango intercuartílico (IQR)
- Detección de outliers con el **método IQR** (límites Q1 − 1.5·IQR y Q3 + 1.5·IQR)
- Cálculo de **Z-Scores** y detección de outliers con `|Z| > 3`
- Comparación entre ambos métodos (coincidencias, diferencias)
- Reporte final de transacciones de alta prioridad (detectadas por ambos métodos)
- Análisis de correlación entre categorías de gasto

## 📦 Requisitos

- Python 3.9+
- NumPy

```bash
pip install numpy
```

## ▶️ Uso

1. Abre Jupyter Notebook / JupyterLab o Google Colab.
2. Pega el código en una celda (o divídelo en varias siguiendo las secciones marcadas con `═══`).
3. Ejecuta de principio a fin (Run All).

No requiere archivos externos: los datos se generan con `np.random.seed(2024)` para resultados reproducibles.

## 🗂️ Estructura de los datos

| Variable | Shape / Tipo | Descripción |
|---|---|---|
| `montos_matriz` | (5, 500) | Montos por categoría (filas) y transacción (columnas) |
| `todos_montos` | (2500,) | Todos los montos concatenados |
| `todas_categorias` | (2500,) | Etiqueta de categoría por transacción |
| `todos_ids` | (2500,) | Identificador único por transacción |
| `zscores_matriz` | (5, 500) | Z-Score de cada transacción por categoría |

Categorías e índices: `0` Supermercados, `1` Restaurantes, `2` Gasolineras, `3` Tiendas_Online, `4` Entretenimiento.

## 📊 Secciones del análisis

1. **Estadísticas por Categoría** — media, mediana, std, min/max, cuartiles, IQR y límites de outliers.
2. **Detección con IQR** — máscara booleana por categoría, conteo de outliers inferiores/superiores, top 3 montos más altos.
3. **Detección con Z-Score** — cálculo de Z-Score (`(x - media) / std`), detección con umbral ±3, separación en outliers altos y bajos.
4. **Comparación y Reporte Final** — outliers totales por método, coincidencias (intersección de IDs), transacciones de "alta prioridad" detectadas por ambos métodos, y resumen ejecutivo con el % de anomalías sobre el total.
5. **Análisis de Correlación (bonus)** — matriz de correlación entre categorías (`np.corrcoef`) y el par con mayor correlación.

## ✅ Notas

- Los outliers detectados son consistentes con el rango esperado (~3–5% por categoría).
- Los Z-Scores se verifican con media ≈ 0 y desviación estándar ≈ 1.
- Reproducible: misma semilla (`2024`) → mismos resultados siempre.
- Probado de inicio a fin sin errores.

