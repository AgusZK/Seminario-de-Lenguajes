import streamlit as st 
import pandas as pd
import sys
from pathlib import Path
import plotly.express as px

# Ajuste para importar módulos propios
sys.path.append(str(Path(__file__).resolve().parents[2]))
from pipeline.rutas import HOGARES_PROCESADOS_PATH, VALORES_CANASTA
from utils.analisis_ingresos import cargar_datos, obtener_opciones_anio_trimestre, analizar_hogares

st.set_page_config(
    page_title="Ingresos",
    page_icon="📊",
    layout="centered"
)

st.markdown("""### Análisis de Ingresos y Línea de Pobreza 📊 """)

st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def cargar_datos_cached():
    return cargar_datos(HOGARES_PROCESADOS_PATH, VALORES_CANASTA)

@st.cache_data(show_spinner=False)
def obtener_opciones_cached(hogares_df):
    return obtener_opciones_anio_trimestre(hogares_df)

# --- Carga de datos
with st.spinner("Cargando datos..."):
    hogares, canasta = cargar_datos_cached()

# --- Selector año y trimestre
st.markdown("#### Seleccioná el año y trimestre")
opciones_lista = obtener_opciones_cached(hogares)
seleccion = st.selectbox("", options=opciones_lista,
                         format_func=lambda x: f"Año {x[0]}, {x[1]}° trimestre")

# --- Botón de análisis
if st.button("Mostrar análisis"):
    st.markdown("<br>", unsafe_allow_html=True)
    año_sel, trimestre_sel = seleccion

    total, pobres, indigentes, CBT, CBA, df_grafico = analizar_hogares(hogares, canasta, año_sel, trimestre_sel)

    if total is None:
        st.warning("No hay datos para esa combinación de año y trimestre.")
        st.stop()

    st.info(f"Resultados para el año {año_sel} - Trimestre {trimestre_sel}")
    st.markdown(f"Hogares de 4 integrantes analizados: **{total}**")
    st.markdown(f"Por debajo de la línea de **pobreza**: **{pobres}** ({pobres/total:.2%})")
    st.markdown(f"Por debajo de la línea de **indigencia**: **{indigentes}** ({indigentes/total:.2%})")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🏠 Hogares según situación económica estimada")
    st.bar_chart(df_grafico.set_index("Categoría"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🏠 Representación proporcional de los mismos indicadores")
    fig = px.pie(
        df_grafico,
        names="Categoría",
        values="Cantidad",
        color="Categoría",
        color_discrete_sequence=["#FFA07A", "#FF6347", "#90EE90"],
        hole=0.4
    )
    fig.update_traces(textinfo='percent+label', pull=[0.05]*len(df_grafico))
    st.plotly_chart(fig, use_container_width=True)
