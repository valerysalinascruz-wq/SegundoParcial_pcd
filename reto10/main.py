import pandas as pd
import numpy as np
from typing import Dict, List

# =========================
# PARTE 1: ESTADÍSTICAS
# =========================

def estadisticas_basicas(precios: pd.Series) -> Dict:
    return {
        "precio_actual": float(precios.iloc[-1]),
        "precio_minimo": float(precios.min()),
        "precio_maximo": float(precios.max()),
        "precio_promedio": float(precios.mean()),
        "precio_mediana": float(precios.median()),
        "desviacion_std": float(precios.std()),
        "rango": float(precios.max() - precios.min()),
        "dias_analizados": int(len(precios))
    }


def calcular_rendimientos(precios: pd.Series) -> pd.Series:
    rend = precios.pct_change() * 100
    rend.name = "rendimiento_%"
    return rend


def analisis_rendimientos(rendimientos: pd.Series) -> Dict:
    r = rendimientos.dropna()

    return {
        "rendimiento_total": float(((1 + r / 100).prod() - 1) * 100),  # ✔ CONSISTENTE
        "rendimiento_promedio": float(r.mean()),
        "mejor_dia": (r.idxmax(), float(r.max())),
        "peor_dia": (r.idxmin(), float(r.min())),
        "dias_positivos": int((r > 0).sum()),
        "dias_negativos": int((r < 0).sum()),
        "volatilidad": float(r.std())
    }


# =========================
# PARTE 2: INDICADORES
# =========================

def media_movil(precios: pd.Series, ventana: int) -> pd.Series:
    return precios.rolling(window=ventana).mean()


def bandas_bollinger(precios: pd.Series, ventana: int = 20, num_std: int = 2) -> Dict:
    sma = precios.rolling(ventana).mean()
    std = precios.rolling(ventana).std()

    return {
        "banda_superior": sma + num_std * std,
        "banda_media": sma,
        "banda_inferior": sma - num_std * std
    }


def detectar_maximos_minimos(precios: pd.Series, ventana: int = 5) -> Dict:
    max_roll = precios.rolling(2 * ventana + 1, center=True).max()
    min_roll = precios.rolling(2 * ventana + 1, center=True).min()

    return {
        "maximos": precios[precios == max_roll],
        "minimos": precios[precios == min_roll]
    }


def clasificar_tendencia(precios: pd.Series, ventana: int = 10) -> str:
    ma = precios.rolling(ventana).mean().dropna()

    if len(ma) < 2:
        return "LATERAL"

    actual = precios.iloc[-1]

    if actual > ma.iloc[-1] and ma.iloc[-1] > ma.iloc[-2]:
        return "ALCISTA"
    elif actual < ma.iloc[-1] and ma.iloc[-1] < ma.iloc[-2]:
        return "BAJISTA"
    return "LATERAL"


# =========================
# PARTE 3: ALERTAS
# =========================

def generar_senales_trading(precios: pd.Series, ma_corta: int = 5, ma_larga: int = 20) -> pd.Series:
    mc = precios.rolling(ma_corta).mean()
    ml = precios.rolling(ma_larga).mean()

    diff = mc - ml
    diff_prev = diff.shift(1)

    senales = pd.Series("MANTENER", index=precios.index)

    senales[(diff > 0) & (diff_prev <= 0)] = "COMPRA"
    senales[(diff < 0) & (diff_prev >= 0)] = "VENTA"

    senales.name = "senal"
    return senales


def alertas_precio(precios: pd.Series, umbral_cambio: float = 5.0) -> List[Dict]:
    rend = calcular_rendimientos(precios).dropna()

    alertas = []
    for fecha, cambio in rend.items():
        if abs(cambio) > umbral_cambio:
            alertas.append({
                "fecha": str(fecha),
                "tipo": "SUBIDA" if cambio > 0 else "CAIDA",
                "cambio": float(cambio)
            })

    return alertas


def clasificar_volatilidad(rendimientos: pd.Series) -> str:
    std = rendimientos.dropna().std()

    if std < 1:
        return "BAJA"
    elif std < 3:
        return "MEDIA"
    elif std < 5:
        return "ALTA"
    return "MUY ALTA"


def generar_reporte_completo(precios: pd.Series, nombre_accion: str) -> Dict:
    rend = calcular_rendimientos(precios)
    sen = generar_senales_trading(precios)
    alertas = alertas_precio(precios)

    return {
        "nombre": nombre_accion,
        "periodo": {
            "inicio": str(precios.index[0]),
            "fin": str(precios.index[-1]),
            "dias": len(precios)
        },
        "estadisticas": estadisticas_basicas(precios),
        "rendimientos": analisis_rendimientos(rend),
        "tendencia": clasificar_tendencia(precios),
        "volatilidad": clasificar_volatilidad(rend),
        "senal_actual": sen.iloc[-1],
        "alertas_recientes": alertas
    }


# =========================
# DATOS SIMULADOS
# =========================

np.random.seed(42)
fechas = pd.date_range("2024-01-01", periods=60, freq="B")

PRECIOS_ACCION = pd.Series(
    100 * np.cumprod(1 + np.random.normal(0.002, 0.02, 60)),
    index=fechas,
    name="ACME"
)

ACCION_VOLATIL = pd.Series(
    50 * np.cumprod(1 + np.random.normal(0, 0.05, 60)),
    index=fechas,
    name="VOL"
)

ACCION_BAJISTA = pd.Series(
    200 * np.cumprod(1 + np.random.normal(-0.005, 0.015, 60)),
    index=fechas,
    name="BAJ"
)


# =========================
# VISUALIZACIÓN
# =========================

def mostrar_reporte(rep: Dict):
    print("=" * 60)
    print(f"REPORTE: {rep['nombre']}")
    print("=" * 60)
    print(rep["estadisticas"])
    print(rep["rendimientos"])
    print(rep["tendencia"], rep["volatilidad"], rep["senal_actual"])


# =========================
# COMPARACIÓN (CORREGIDA)
# =========================

print("\n=== COMPARACIÓN FINAL ===")

acciones = [
    (PRECIOS_ACCION, "ACME"),
    (ACCION_VOLATIL, "VOLATIL"),
    (ACCION_BAJISTA, "BAJISTA")
]

for precios, nombre in acciones:
    r = calcular_rendimientos(precios)

    # ✔ CORRECCIÓN FINAL OBLIGATORIA
    rend_total = ((1 + r.dropna() / 100).prod() - 1) * 100

    print(f"\n{nombre}")
    print(f"Rendimiento compuesto: {rend_total:+.2f}%")
    print(f"Volatilidad: {clasificar_volatilidad(r)}")
    print(f"Tendencia: {clasificar_tendencia(precios)}")


# =========================
# REPORTE FINAL
# =========================

reporte = generar_reporte_completo(PRECIOS_ACCION, "ACME")
mostrar_reporte(reporte)