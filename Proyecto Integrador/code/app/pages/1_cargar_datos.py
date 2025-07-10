import streamlit as st
from pathlib import Path
import sys
import csv

sys.path.append(str(Path(__file__).resolve().parents[2]))
import pipeline.procesamiento as procesamiento
from pipeline.rutas import INDIVIDUOS_PATH, HOGARES_PATH, HOGARES_PROCESADOS_PATH
from utils.archivos import (
    extraer_periodo_desde_txt,
    verificar_pares_archivos,
    ya_esta_registrado
)

st.set_page_config(
    page_title="Cargar datos",
    page_icon="📤",
    layout="wide"
)

dataset_path = HOGARES_PROCESADOS_PATH

@st.cache_data(show_spinner=False)
def obtener_rango_fechas_cached(path):
    return procesamiento.obtener_rango_fechas(path)

# Inicializar estado
if "rango_fechas" not in st.session_state:
    if dataset_path.exists():
        try:
            st.session_state.rango_fechas = obtener_rango_fechas_cached(dataset_path)
        except Exception:
            st.session_state.rango_fechas = "Error al leer el archivo."
    else:
        st.session_state.rango_fechas = "Aún no hay datos cargados."

if "archivos_nuevos_subidos" not in st.session_state:
    st.session_state.archivos_nuevos_subidos = False

# Mostrar rango de fechas
st.info(st.session_state.rango_fechas)
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Cargar nuevos datos")
st.markdown("<br>", unsafe_allow_html=True)

archivo_individuos = st.file_uploader("📂 Subí el archivo de individuos", type=["txt"])
archivo_hogares = st.file_uploader("📂 Subí el archivo de hogares", type=["txt"])

if archivo_individuos and archivo_hogares:
    anio, trimestre = extraer_periodo_desde_txt(archivo_hogares.getvalue())
    archivo_hogares.seek(0)

    if ya_esta_registrado(anio, trimestre, dataset_path):
        st.warning(f"Los datos del {trimestre}º trimestre del año {anio} ya están registrados. No se cargaron.")
    else:
        INDIVIDUOS_PATH.mkdir(parents=True, exist_ok=True)
        HOGARES_PATH.mkdir(parents=True, exist_ok=True)

        with open(INDIVIDUOS_PATH / archivo_individuos.name, "wb") as f:
            f.write(archivo_individuos.getbuffer())

        with open(HOGARES_PATH / archivo_hogares.name, "wb") as f:
            f.write(archivo_hogares.getbuffer())

        st.session_state.archivos_nuevos_subidos = True
        st.success("Archivos cargados correctamente.")

st.markdown("<br>", unsafe_allow_html=True)

st.info("📌 Podes actualizar la base de datos actual con el siguiente boton. Si cargaste nuevos archivos se sumaran a nuestra base de datos")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Actualizar base de datos"):
    hay_datos = any(HOGARES_PATH.glob("*.txt")) and any(INDIVIDUOS_PATH.glob("*.txt"))

    if hay_datos:
        with st.spinner("Estamos preparando tus datos... ¡Ya casi terminamos!"):
            procesamiento.unir_ambos_archivos()
            procesamiento.reemplazar_ambos_archivos()

        st.cache_data.clear()
        st.session_state.rango_fechas = obtener_rango_fechas_cached(dataset_path)
        st.success("¡Listo! Ya podés consultar y visualizar las estadísticas con la nueva información.")
        st.session_state.archivos_nuevos_subidos = False
    else:
        st.warning("No se encontraron archivos para procesar.")

# Verificación de pares
st.markdown("---")
st.subheader("Verificación de pares de archivos cargados")

inconsistencias = verificar_pares_archivos(HOGARES_PATH, INDIVIDUOS_PATH)

if inconsistencias:
    st.warning("Se encontraron los siguientes archivos sin su par correspondiente:")
    for anio, trimestre, faltante in inconsistencias:
        st.write(f"• Falta archivo de **{faltante}** para {trimestre}° trimestre de {anio}")
else:
    st.success("Verificamos que todos los archivos tienen su par correspondiente al mismo periodo.")
