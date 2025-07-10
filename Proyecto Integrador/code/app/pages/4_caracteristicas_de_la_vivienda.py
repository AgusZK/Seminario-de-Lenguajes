import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from pipeline.rutas import HOGARES_PROCESADOS_PATH

# Mapa de aglomerados
mapa_aglomerados = {
    2: "Gran La Plata",3: "Bahía Blanca-Cerri",4: "Gran Rosario",5: "Gran Santa Fe",6: "Gran Paraná",7: "Posadas",8: "Gran Resistencia",9: "Comodoro Rivadavia-Rada Tilly",10: "Gran Mendoza",
    12: "Corrientes",13: "Gran Córdoba",14: "Concordia",15: "Formosa",17: "Neuquén-Plottier",18: "Santiago del Estero-La Banda",19: "Jujuy-Palpalá",
    20: "Río Gallegos",22: "Gran Catamarca",23: "Gran Salta",25: "La Rioja",26: "Gran San Luis",27: "Gran San Juan", 29: "Gran Tucumán-Tafí Viejo",
    30: "Santa Rosa-Toay",31: "Ushuaia-Río Grande",32: "Ciudad Autónoma de Buenos Aires",33: "Partidos del GBA",34: "Mar del Plata",36: "Río Cuarto",38: "San Nicolás-Villa Constitución",
    40: "Resto Buenos Aires",41: "Resto Catamarca",42: "Resto Córdoba",43: "Resto Corrientes",44: "Resto Chaco",45: "Resto Chubut",46: "Resto Entre Ríos",47: "Resto Formosa",48: "Resto Jujuy",49: "Resto La Pampa",
    50: "Resto La Rioja",51: "Resto Mendoza",52: "Resto Misiones",53: "Resto Neuquén",54: "Resto Río Negro",55: "Resto Salta",56: "Resto San Juan",57: "Resto San Luis",58: "Resto Santa Cruz",
    60: "Resto Santa Fe",61: "Resto Santiago del Estero",62: "Resto Tucumán",
    91: "Rawson-Trelew",93: "Viedma-Carmen de Patagones"
}

st.title(" Caracteristicas de la vivienda") #Titulo de la pagina 1.4.1 -


def carga_de_datos():
    
    df_hogares = pd.read_csv(HOGARES_PROCESADOS_PATH, sep=";",encoding="utf-8")
    
    return df_hogares

df_hogares = carga_de_datos()

anios_disponibles = sorted(df_hogares['ANO4'].unique())

anio_seleccionado = st.selectbox("Seleccione un año", options = ["Todos"] +list(anios_disponibles))

if anio_seleccionado != "Todos":
    hogares_filtrados = df_hogares[df_hogares["ANO4"] == anio_seleccionado]
else:    
    hogares_filtrados = df_hogares

cantidad_viviendas = hogares_filtrados["CODUSU"].nunique()

st.subheader("Cantidad total de viviendas en la escuesta")

st.write(f"{cantidad_viviendas:,}viviendas encontradas")

st.subheader(" Proporcion de viviendas segun su tipo ")  #1.4.2 -
mapa_tipos_vivienda = {
    1: "Casa",
    2: "Departamento",
    3: "pieza de inquilinato",
    4: "pieza de hotel/pension",
    5: "local no construido para habitacion",
}

hogares_filtrados["TIPO_VIV"] = hogares_filtrados["IV1"].map(mapa_tipos_vivienda)
conteo = hogares_filtrados["TIPO_VIV"].value_counts()


fig, ax = plt.subplots()

# Calcular porcentajes
porcentajes = (conteo / conteo.sum() * 100).round(1)
labels_con_porcentaje = [f"{tipo} ({porc}%)" for tipo, porc in zip(conteo.index, porcentajes)]

# Gráfico
ax.pie(conteo, labels=None, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
ax.set_title("Proporción de viviendas según su tipo")
ax.legend(labels_con_porcentaje, loc="center left", bbox_to_anchor=(1, 0.5))

st.pyplot(fig)

st.subheader("Material predominante en pisos por aglomerado")  #1.4.3 - 
pisos = {
    1: "Mosaico",
    2: "Cemento fijo",
    3: "Ladrillo suelto"
    }

predominante = hogares_filtrados.groupby("AGLOMERADO")["IV3"]\
    .agg(lambda x: x.mode().iloc[0])\
    .rename("Material")\
    .reset_index()

predominante["Material"] = predominante["Material"].map(pisos)


predominante["Aglomerado"] = predominante["AGLOMERADO"].map(mapa_aglomerados)


predominante = predominante[["Aglomerado", "Material"]]

st.write(predominante)


st.subheader(" Porcentaje de viviendas con baño dentro del hogar")  #1.4.4 -
df_hogares["IV8"] = df_hogares["IV8"].apply(lambda x: 1 if x == 1 else 0)
porcentaje_bano = (df_hogares.groupby("AGLOMERADO")["IV8"].mean() * 100).round(2).rename("Porcentaje")
st.write(porcentaje_bano.round(2))

hogares_filtrados["IV8"] = hogares_filtrados["IV8"].apply(lambda x: 1 if x == 1 else 0)
porcentaje_bano = hogares_filtrados.groupby("AGLOMERADO")["IV8"].mean().round(4) * 100


porcentaje_bano.index = porcentaje_bano.index.map(mapa_aglomerados)

st.bar_chart(porcentaje_bano)


st.subheader(" Evolución del régimen de tenencia")  #1.4.5 -

agloms = sorted(df_hogares["AGLOMERADO"].unique())
aglom_seleccionado = st.selectbox("Seleccione aglomerado", agloms)


df_aglom = df_hogares[df_hogares["AGLOMERADO"] == aglom_seleccionado]
nombre_aglom = mapa_aglomerados.get(aglom_seleccionado, f"Aglomerado {aglom_seleccionado}")

mapa_tenencia = {
    1: "Propietario de vivienda y el terreno",
    2: "Propietario de la vivienda solamente",
    3: "Inquilino/arrendatario de la vivienda",
    4: "Ocupante por pago de impuestos/expensas",
    5: "Ocupante por relacion de dependencia",
    6: "Ocupante gratuito(con permiso)",
    7: "Ocupante de hecho(sin permiso)",
    8: "Esta en sucesion"
}

df_aglom["II7_nombre"] = df_aglom["II7"].map(mapa_tenencia)
tipos_tenencia = df_aglom["II7_nombre"].dropna().unique()
tenencias_seleccionadas = st.multiselect("Seleccione tipo de tenencia", opciones := list(tipos_tenencia), default=opciones)

df_filtrado = df_aglom[df_aglom["II7_nombre"].isin(tenencias_seleccionadas)]
evolucion = df_filtrado.groupby(["ANO4", "II7_nombre"]).size().unstack().fillna(0)

st.line_chart(evolucion)



st.subheader("Viviendas en villa por aglomerado")  #1.4.6 -


hogares_filtrados["IV12_3"] = hogares_filtrados["IV12_3"].apply(lambda x: 1 if x == 1 else 0)

total_viv = hogares_filtrados.groupby("AGLOMERADO")["CODUSU"].nunique()
viv_villa = hogares_filtrados[hogares_filtrados["IV12_3"] == 1].groupby("AGLOMERADO")["CODUSU"].nunique()

result = pd.DataFrame({
    "Viviendas en villa": viv_villa,
    "Total viviendas": total_viv,
    "Porcentaje": (viv_villa / total_viv * 100).round(2)
}).fillna(0)

result["Aglomerado"] = result.index.map(mapa_aglomerados)
result = result.set_index("Aglomerado").sort_values(by="Porcentaje", ascending=False)

st.dataframe(result)

st.bar_chart(result["Porcentaje"])


st.subheader("Condición de habitabilidad por aglomerado")  #1.4.7 -
porcentajes = (hogares_filtrados.groupby(["AGLOMERADO", "CONDICION_DE_HABITABILIDAD"])
               .size()
               .groupby(level=0)
               .apply(lambda x: (x / x.sum() * 100).round(2))
               .unstack()
               .fillna(0)
)

porcentajes.index = porcentajes.index.map(mapa_aglomerados)
st.dataframe(porcentajes)


csv = porcentajes.to_csv().encode("utf-8")                              
st.download_button("Descargar como CSV", data=csv, file_name="habitabilidad_por_aglomerado.csv", mime="text/csv")