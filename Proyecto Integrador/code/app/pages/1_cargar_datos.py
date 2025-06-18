import streamlit as st
from pathlib import Path
import sys
import csv

# Asegura que el directorio raíz del proyecto esté en sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pipeline.procesamiento as procesamiento
from pipeline.rutas import INDIVIDUOS_PATH, HOGARES_PATH, PROCESADOS_PATH

# Ruta completa del archivo procesado
dataset_path = PROCESADOS_PATH / "hogares.csv"

# Inicializar rango de fechas en session_state
if "rango_fechas" not in st.session_state:
    if dataset_path.exists():
        try:
            st.session_state.rango_fechas = procesamiento.obtener_rango_fechas(dataset_path)
        except Exception:
            st.session_state.rango_fechas = "Error al leer el archivo."
    else:
        st.session_state.rango_fechas = "Aún no hay datos cargados. Subí los archivos y hacé clic en 'Actualizar base de datos'."

# Inicializar bandera para archivos nuevos
if "archivos_nuevos_subidos" not in st.session_state:
    st.session_state.archivos_nuevos_subidos = False

# Mostrar el mensaje actual de rango de fechas
st.info(st.session_state.rango_fechas)

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Podés cargar nuevos datos y actualizar la base de consulta")
st.markdown("<br>", unsafe_allow_html=True)

# Cargar archivos
archivo_individuos = st.file_uploader("📂 Subí el archivo de individuos", type=["txt"])
archivo_hogares = st.file_uploader("📂 Subí el archivo de hogares", type=["txt"])

def extraer_periodo_desde_txt(archivo_stream):
    """Devuelve una tupla (anio, trimestre) desde archivo txt en memoria."""
    archivo_stream.seek(0)
    decoded = archivo_stream.read().decode("utf-8").splitlines()
    lector = csv.DictReader(decoded, delimiter=";")

    for fila in lector:
        fila = {key.strip(): value.strip() for key, value in fila.items()}
        if fila.get("ANO4", "").isdigit() and fila.get("TRIMESTRE", "").isdigit():
            return int(fila["ANO4"]), int(fila["TRIMESTRE"])
    return None, None



def ya_esta_registrado(anio, trimestre, dataset_path):
    if not dataset_path.exists():
        return False
    with open(dataset_path, encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=';') 
        for fila in lector:
            if int(fila["ANO4"]) == anio and int(fila["TRIMESTRE"]) == trimestre:
                return True
    return False


# Si ambos archivos fueron subidos
if archivo_individuos and archivo_hogares:
    # Validar duplicados
    anio, trimestre = extraer_periodo_desde_txt(archivo_hogares)
    archivo_hogares.seek(0)  # Volver a inicio para guardar después

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

# Estado para mostrar el mensaje de éxito después del procesamiento
mostrar_mensaje_exito = False

# Botón de procesamiento
if st.button("Actualizar base de datos"):
    if st.session_state.archivos_nuevos_subidos:
        with st.spinner("Estamos preparando tus datos... ¡Ya casi terminamos!"):
            procesamiento.unir_ambos_archivos()
            procesamiento.reemplazar_ambos_archivos()

        # Actualizar el rango de fechas después de procesar
        st.session_state.rango_fechas = procesamiento.obtener_rango_fechas(dataset_path)
        mostrar_mensaje_exito = True

        # Limpiar bandera
        st.session_state.archivos_nuevos_subidos = False
    else:
        st.warning("Primero cargá nuevos archivos para actualizar.")

# Mostrar mensaje de éxito debajo del botón (solo si se procesó)
if mostrar_mensaje_exito:
    st.success("¡Listo! Ya podés consultar y visualizar las estadísticas con la nueva información que añadiste.")
