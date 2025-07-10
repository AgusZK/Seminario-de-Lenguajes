from pathlib import Path
import streamlit as st
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import json
from streamlit_folium import st_folium
sys.path.append(str(Path(__file__).resolve().parents[2]))
from utils.pag5 import *
from pipeline.rutas import PROCESADOS_PATH, AGLOMERADOS_COORDENADAS


def mostrar_evolucion_empleo_y_desempleo(df_individuos, df_aglomerados):
    """ Recibe el DataFrame por parametro y muestra en un grafico de lineas la tasa de empleo y desempleo 
    respectivamente en un aglomerado seleccionado, en caso de no elegir lo muestra en todo el pais""" 
    
    st.markdown("<h2><u>Evolución del empleo y desempleo</u></h2>", unsafe_allow_html=True)
    # Selector de aglomerado
    nombres_aglomerados = df_aglomerados['nombre'].sort_values().tolist()
    nombre_elegido = st.selectbox("Filtrar por aglomerado", ['Todo el pais'] + nombres_aglomerados)

    if nombre_elegido != 'Todo el pais':
        aglomerado_id = df_aglomerados[df_aglomerados['nombre'] == nombre_elegido]['aglomerado'].values[0]
        df_individuos = df_individuos[df_individuos['AGLOMERADO'] == aglomerado_id]
        sufijo = f"({nombre_elegido})"
    else:
        sufijo = "(todo el país)"

    # LLAMO A CALCULO DEL DF PARA EL GRAFICO
    df_tasas = calcular_evolucion_empleo_y_desempleo(df_individuos,df_aglomerados)

    # Creo figura con dos subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

    # Grafico de tasa de desempleo
    axes[0].plot(df_tasas['Anio/Trim'], df_tasas['Tasa de desempleo'], marker='o', color='red')
    axes[0].set_title(f"Tasa de Desempleo {sufijo}")
    axes[0].set_xlabel('Año/Trimestre')
    axes[0].set_ylabel('%')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True)

    # Grafico de tasa de empleo
    axes[1].plot(df_tasas['Anio/Trim'], df_tasas['Tasa de empleo'], marker='o', color='green')
    axes[1].set_title(f"Tasa de Empleo {sufijo}")
    axes[1].set_xlabel('Año/Trimestre')
    axes[1].set_ylabel('%')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True)

    st.pyplot(fig)
    plt.clf()


def mostrar_porcentajes_de_empleo(df_individuos):
    """ Recibe el DataFrame por parametro y muestra en un grafico de barras agrupadas el porcentaje de 
     los diferentes tipos de empleo registrados""" 
    
    st.markdown("<h2><u>Porcentaje de empleo estatal/privado/otros</u></h2>", unsafe_allow_html=True)

    # LLAMO A CALCULO DE DF PARA EL GRAFICO
    resultado = calcular_porcentajes_de_empleo(df_individuos)

    # GRAFICO
    df_plot = resultado.reset_index()[['AGLOMERADO', 'Estatal', 'Privado', 'Otro tipo', 'Total ocupados']]
    # LO PASO A FORMATO LARGO PARA USARLO EN PLOTLY
    df_melted = df_plot.melt(
        id_vars=['AGLOMERADO', 'Total ocupados'],
        value_vars=['Estatal', 'Privado', 'Otro tipo'],
        var_name='Tipo de Empleo',
        value_name='Porcentaje'
    )

    fig = px.bar(df_melted,x='AGLOMERADO',y='Porcentaje',color='Tipo de Empleo',barmode='group',
        hover_data={
            'AGLOMERADO': True,
            'Tipo de Empleo': True,
            'Porcentaje': ':.2f',
            'Total ocupados': True
        },
    )

    fig.update_layout(xaxis_title='Aglomerado', yaxis_title='Porcentaje',legend_title='Tipo de empleo',height=600,width=800)

    fig.update_xaxes(
        type='category', # LO PASO A CATEGORICO PARA QUE NO HAYA ESPACIOS
        categoryorder='array',
        categoryarray=resultado.index.tolist(),  # ORDEN DE LOS AGLOMERADOS DISPONIBLES
        tickangle=0                         
    )

    # LO MUESTRO Y LE SACO OPCIONES DE MENU EXTRA MOLESTAS, DEJO SOLO FULL SCREEN
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',  'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage', 'sendDataToCloud', 'toggleSpikelines']})

def mostrar_desocupados_segun_educacion(df_individuos):
    """Muestra un grafico de barras con la cantidad de personas desocupadas segun el nivel educativo alcanzado."""

    st.markdown("<h2><u>Distribucion de personas desocupadas segun su nivel educativo</u></h2>", unsafe_allow_html=True)

    # Obtengo los anos disponibles, ordenados
    anios_disponibles = sorted(df_individuos['ANO4'].dropna().unique())

    # Elijo el año (solo los que existen)
    anio = st.selectbox("Elegí el año:", anios_disponibles)

    # Para ese año, muestro solo los trimestres que existen
    trimestres_disponibles = sorted(df_individuos[df_individuos['ANO4'] == anio]['TRIMESTRE'].unique())
    trimestre = st.selectbox("Elegí el trimestre:", trimestres_disponibles)

    resultado = calcular_desocupados_segun_educacion(df_individuos, anio, trimestre)   

    # Grafico de barras
    fig, ax = plt.subplots(figsize=(10, 5))
    resultado.plot(kind='bar', ax=ax)
    ax.set_title(f'Cantidad de personas desocupadas segun nivel educativo\nAño: {anio}, Trimestre: {trimestre}')
    ax.set_xlabel('Nivel educativo')
    ax.set_ylabel('Cantidad de personas')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.clf()

def mostrar_mapa(df, df_coordenadas):
    """Muestra un mapa con círculos según el cambio en la tasa de empleo o desempleo por aglomerado."""

    st.markdown("<h2><u>Evolución de la Tasa de Empleo o Desempleo por Aglomerado</u></h2>", unsafe_allow_html=True)

    # Muestro para seleccion la tasa de empleo o desempleo
    tipo = st.selectbox("Elegí ver tasa de empleo o desempleo:", ['empleo', 'desempleo'])
    
    # Estandarizo el texto
    df['CONDICION_LABORAL'] = df['CONDICION_LABORAL'].str.lower()

    # Determino los años/trimestres extremos
    min_anio = df['ANO4'].min()
    min_trim = df[df['ANO4'] == min_anio]['TRIMESTRE'].min()
    max_anio = df['ANO4'].max()
    max_trim = df[df['ANO4'] == max_anio]['TRIMESTRE'].max()

    # Filtro los dataframes de inicio y fin
    df_inicio = df[(df['ANO4'] == min_anio) & (df['TRIMESTRE'] == min_trim)]
    df_fin = df[(df['ANO4'] == max_anio) & (df['TRIMESTRE'] == max_trim)]

    # Creo mapa base con capa para adaptar el mismo
    attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'   
    )

    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'

    
    mapa = folium.Map(location=[-33.457606, -65.346857], zoom_start=4, attr=attr, tiles=tiles)

    # Recorro todos los aglomerados
    for aglo in df['AGLOMERADO'].unique():
        df_i = df_inicio[df_inicio['AGLOMERADO'] == aglo]
        df_f = df_fin[df_fin['AGLOMERADO'] == aglo]

        # Calculo las tasas
        if tipo == 'empleo':
            tasa_i = calcular_tasa_laboral(df_i)
            tasa_f = calcular_tasa_laboral(df_f)
        else:
            tasa_i = calcular_tasa_laboral(df_i, 'desempleo')
            tasa_f = calcular_tasa_laboral(df_f, 'desempleo')

        # Determino si mejoro o empeoro
        cambio_positivo = tasa_f > tasa_i

        # Asigno color segun si es empleo o desempleo y si mejoro o empeoro
        if tipo == 'empleo':
            color = 'green' if cambio_positivo else 'red'
        else: 
            color = 'red' if cambio_positivo else 'red'

        # Busco coordenadas y nombre
        fila = df_coordenadas[df_coordenadas['aglomerado'] == aglo].iloc[0]
        nombre = fila['nombre']
        lat, lon = fila['coordenadas']

        folium.CircleMarker(
            location=[lat, lon],
            radius=7,
            color=color,
            fill=True,
            fill_color=color
         ).add_to(mapa)

    # Muestro en Streamlit
    st_folium(mapa)

if __name__ == "__main__":
     st.title('Actividad y Empleo')
     file = PROCESADOS_PATH/'individuos.csv'
     try:
         df_individuos = pd.read_csv(file, sep=';', low_memory=False)
         df_coordenadas = pd.read_json(AGLOMERADOS_COORDENADAS, orient='index')
         df_coordenadas.index.name = 'aglomerado'
         df_coordenadas.reset_index(inplace=True)
     except FileNotFoundError as e:  
           st.error(f'No se ha encontrado el archivo {e.filename} para realizar las consultas')
     except UnicodeDecodeError as e:
         st.error(f'Ha ocurrido un error de formato al intentar leer el archivo {e}')
     except json.JSONDecodeError as e:
         st.error(f'El contenido del archivo JSON no es valido: {e}')
     except Exception as e:
         print(f'Ocurrio un error inesperado: {e}')
     else:
        mostrar_desocupados_segun_educacion(df_individuos)
        mostrar_evolucion_empleo_y_desempleo(df_individuos, df_coordenadas)
        mostrar_porcentajes_de_empleo(df_individuos)
        mostrar_mapa(df_individuos, df_coordenadas)
