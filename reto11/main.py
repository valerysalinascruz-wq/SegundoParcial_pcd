import pandas as pd
import numpy as np
from typing import Dict, Tuple
from datetime import datetime


# =========================================================
# UTILIDADES
# =========================================================

def calcular_promedio(df):
    """Promedio seguro ignorando NaN"""
    return df[['parcial_1','parcial_2','final']].mean(axis=1, skipna=True)


def safe_div(a, b):
    return a / b if b != 0 else 0


# =========================================================
# PARTE 1: CARGA + LIMPIEZA
# =========================================================

def cargar_datos() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    np.random.seed(42)

    estudiantes = pd.DataFrame({
        'boleta': ['2021630001','2021630002','2021630003','2021630004','2021630005',
                   '2022630001','2022630002','2022630003','2022630004','2022630005',
                   '2023630001','2023630002','2023630003','2023630004','2023630005'],
        'nombre': ['Juan Pérez García','María López Ruiz','Pedro Sánchez Torres',
                   'Ana Martínez Díaz','Luis Rodríguez Vega','Carmen Flores Luna',
                   'Roberto Díaz Mora','Laura Torres Silva','Diego Ramírez Cruz',
                   'Sofía Vargas Romo','Carlos Mendoza Ríos','Patricia Ortiz León',
                   'Miguel Ángel Castro','Fernanda Reyes Paz','Andrés Guzmán Villa'],
        'semestre': [4,4,4,4,4,3,3,3,3,3,2,2,2,2,2],
        'carrera': ['CD']*15,
        'email': ['a@ipn.mx']*15
    })

    materias = pd.DataFrame({
        'materia_id': ['MAT101','MAT102','PROG101','PROG102','EST101','EST102','BD101'],
        'nombre': ['Cálculo Diferencial','Cálculo Integral','Programación I',
                   'Programación II','Probabilidad','Estadística Inferencial','Bases de Datos'],
        'creditos': [8,8,6,6,6,6,6],
        'semestre': [1,2,1,2,2,3,3]
    })

    data = []

    for b in estudiantes['boleta']:
        semestre = estudiantes.loc[estudiantes.boleta==b,'semestre'].values[0]
        mats = materias[materias.semestre <= semestre].materia_id

        for m in mats:
            base = np.random.uniform(5,10)

            p1 = np.clip(base + np.random.normal(0,1),0,10)
            p2 = np.clip(base + np.random.normal(0,1),0,10)
            fin = np.clip(base + np.random.normal(0,0.5),0,10)

            if np.random.rand() < 0.05:
                p2 = np.nan

            data.append([b,m,p1,p2,fin])

    calificaciones = pd.DataFrame(data,
        columns=['boleta','materia_id','parcial_1','parcial_2','final'])

    # LIMPIEZA BÁSICA
    calificaciones = calificaciones.drop_duplicates()

    return estudiantes, calificaciones, materias


# =========================================================
# PARTE 1: INFO + VALIDACIÓN ROBUSTA
# =========================================================

def info_general(df_est, df_cal):

    try:
        return {
            "total_estudiantes": int(df_est.boleta.nunique()),
            "total_registros_calif": int(len(df_cal)),
            "semestres": sorted(df_est.semestre.unique().tolist()),
            "materias_con_registros": int(df_cal.materia_id.nunique())
        }
    except Exception as e:
        return {"error": str(e)}


def validar_datos(df_cal):

    try:
        cols = ['parcial_1','parcial_2','final']

        nulos = int(df_cal[cols].isna().any(axis=1).sum())

        fuera = int(((df_cal[cols] < 0) | (df_cal[cols] > 10)).any(axis=1).sum())

        return {
            "registros_con_nulos": nulos,
            "calificaciones_fuera_rango": fuera,
            "datos_validos": fuera == 0
        }

    except Exception as e:
        return {"error": str(e)}


# =========================================================
# PARTE 2: CONSULTAS SEGURAS
# =========================================================

def buscar_estudiante(df, criterio, valor):

    try:
        if criterio == "boleta":
            return df[df.boleta == valor]

        if criterio == "nombre":
            return df[df.nombre.str.contains(valor, case=False, na=False)]

        if criterio == "semestre":
            return df[df.semestre == int(valor)]

        return pd.DataFrame()

    except Exception:
        return pd.DataFrame()


def obtener_kardex(boleta, df_est, df_cal, df_mat):

    try:
        est = df_est[df_est.boleta == boleta]
        if est.empty:
            return {"estudiante": None}

        cal = df_cal[df_cal.boleta == boleta].merge(df_mat, on='materia_id')

        cal['promedio'] = calcular_promedio(cal)

        return {
            "estudiante": est.iloc[0].to_dict(),
            "materias": cal,
            "promedio_general": round(cal.promedio.mean(),2) if len(cal)>0 else 0,
            "creditos_cursados": int(cal.creditos.sum()) if len(cal)>0 else 0,
            "materias_aprobadas": int((cal.promedio>=6).sum()),
            "materias_reprobadas": int((cal.promedio<6).sum())
        }

    except Exception as e:
        return {"error": str(e)}


# =========================================================
# PARTE 3: ESTADÍSTICAS ROBUSTAS
# =========================================================

def calcular_promedio_materia(df_cal, materia_id):

    df = df_cal[df_cal.materia_id == materia_id].copy()

    if df.empty:
        return {"materia": materia_id}

    df['prom'] = calcular_promedio(df)

    return {
        "materia": materia_id,
        "inscritos": len(df),
        "promedio_parcial1": round(df.parcial_1.mean(),2),
        "promedio_parcial2": round(df.parcial_2.mean(),2),
        "promedio_final": round(df.final.mean(),2),
        "promedio_general": round(df.prom.mean(),2),
        "tasa_aprobacion": round((df.prom>=6).mean()*100,1),
        "calificacion_maxima": float(df.prom.max()),
        "calificacion_minima": float(df.prom.min())
    }


def ranking_estudiantes(df_cal, df_est, top_n=10):

    df = df_cal.copy()
    df['prom'] = calcular_promedio(df)

    r = df.groupby('boleta')['prom'].mean().reset_index()
    r = r.merge(df_est,on='boleta')
    r = r.sort_values('prom',ascending=False).head(top_n)

    r['prom'] = r.prom.round(2)
    r.insert(0,'posicion',range(1,len(r)+1))

    return r[['posicion','boleta','nombre','semestre','prom']]


def estadisticas_por_semestre(df_est, df_cal):

    df = df_cal.copy()
    df['prom'] = calcular_promedio(df)

    r = df.groupby('boleta')['prom'].mean().reset_index()
    r = r.merge(df_est[['boleta','semestre']], on='boleta')

    g = r.groupby('semestre').agg(
        estudiantes=('boleta','count'),
        promedio=('prom','mean'),
        mejor=('prom','max'),
        peor=('prom','min')
    )

    g['tasa_aprobacion'] = r.groupby('semestre')['prom'].apply(lambda x: safe_div((x>=6).sum(),len(x))*100)

    return g.round(2)


# =========================================================
# PARTE 4: RIESGO + REPORTE PRO
# =========================================================

def identificar_estudiantes_riesgo(df_cal, df_est, umbral=7, max_rep=2):

    df = df_cal.copy()
    df['prom'] = calcular_promedio(df)
    df['rep'] = df.prom < 6

    r = df.groupby('boleta').agg(
        prom=('prom','mean'),
        rep=('rep','sum')
    ).reset_index()

    riesgo = r[(r.prom < umbral) | (r.rep > max_rep)]

    return riesgo.merge(df_est,on='boleta')


def generar_reporte_academico(df_est, df_cal, df_mat):

    try:
        df = df_cal.copy()
        df['prom'] = calcular_promedio(df)

        return {
            "resumen_general": {
                "total_estudiantes": len(df_est),
                "promedio_global": round(df.prom.mean(),2),
                "tasa_aprobacion": round((df.prom>=6).mean()*100,1)
            },
            "por_semestre": estadisticas_por_semestre(df_est, df_cal),
            "por_materia": None,
            "mejores_estudiantes": ranking_estudiantes(df_cal, df_est, 10),
            "estudiantes_riesgo": identificar_estudiantes_riesgo(df_cal, df_est),
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {"error": str(e)}


# =========================================================
# EXPORTACIÓN SEGURA
# =========================================================

def exportar_kardex(boleta, kardex, formato='csv'):

    try:
        df = kardex.get('materias')

        if df is None:
            raise ValueError("Kardex vacío")

        nombre = f"kardex_{boleta}.{formato}"

        if formato == 'csv':
            df.to_csv(nombre,index=False)

        elif formato == 'json':
            df.to_json(nombre,orient='records')

        else:
            raise ValueError("Formato inválido")

        return nombre

    except Exception as e:
        return {"error": str(e)}