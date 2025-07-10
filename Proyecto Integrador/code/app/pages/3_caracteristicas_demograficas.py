from pathlib import Path
import streamlit as st
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import json
sys.path.append(str(Path(__file__).resolve().parents[2]))
from utils.pag3 import *

from pipeline.rutas import PROCESADOS_PATH, AGLOMERADOS_COORDENADAS

def mostrar_promedio(individuos, df_aglomerados):
    """ Recibe el DataFrame por parametro, calcula y muestra en un grafico de barras el promedio de edad 
     del ultimo trimestre del ultimo año registrado"""
    # ME GUARDO ULTIMO ANIO Y TRIM
    ultimo_anio = individuos['ANO4'].max()
    ultimo_trim = individuos[individuos["ANO4"] == ultimo_anio]["TRIMESTRE"].max()
    # MUESTRO EL ULTIMO ANIO Y TRIM CALCULADO EN EL MOMENTO
    st.markdown("<h2><u>Promedio de edades</u></h2>", unsafe_allow_html=True)
    st.info(f'Ultimo año y trimestre registrado: 0{ultimo_trim}/{ultimo_anio}')

    # LLAMO AL CALCULO DE DF PARA EL GRAFICO
    edad_promedio = calcular_promedio(individuos,df_aglomerados)

    fig = px.bar(
        edad_promedio,
        x='AGLOMERADO',
        y='Edad promedio',
        text=None, 
        hover_name='nombre',  
        hover_data={  # MUESTRO SOLO NOMBRE de AGLOMNERADO
            'AGLOMERADO': False,
            'Edad promedio': False,
            'nombre': False  
        },
        labels={'AGLOMERADO': 'Aglomerado', 'Edad promedio': 'Edad promedio'},
        height=600,
        width=900
    )

    fig.update_xaxes(
        type='category', # LO PASO A CATEGORICO PARA QUE NO HAYA ESPACIOS
        categoryorder='array',
        categoryarray=edad_promedio['AGLOMERADO'].tolist(),  # ORDEN DE LOS AGLOMERADOS DISPONIBLES
        tickangle=0                         
    )

    fig.update_layout(
        xaxis_title='Aglomerado',
        yaxis_title='Edad promedio',
        yaxis=dict(range=[edad_promedio['Edad promedio'].min() - 1, edad_promedio['Edad promedio'].max() + 1]) # AJUSTO ALTO PARA QUE SEA MAS PROLIJO
    )
    # LO MUESTRO Y LE SACO OPCIONES DE MENU EXTRA MOLESTAS, DEJO SOLO FULL SCREEN
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',  'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage', 'sendDataToCloud', 'toggleSpikelines']})

def mostrar_media_y_mediana (individuos):
    """ Recibe el DF por parametro y muestra la evolucion de la media y mediana en un grafico de lineas"""
    
    st.markdown("<h2><u>Media y Mediana de edades</u></h2>", unsafe_allow_html=True)
    media_mediana = calcular_media_y_mediana(individuos)

    # GRAFICO
    # CREA ETIQUETA TRIM/ANIO PARA CADA UNO DE LA TUPLA EN EL EJE X, _ IGNORA INDICE  
    etiquetas = [f"0{int(row['TRIMESTRE'])}/{int(row['ANO4'])}" for _, row in media_mediana.iterrows()] 
    x = range(len(etiquetas))
    media = media_mediana['MEDIA']
    mediana = media_mediana['MEDIANA']
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, media, marker='o', label='Media')
    plt.plot(x, mediana, marker='o', label='Mediana')
    plt.xticks(x, etiquetas, rotation=45)
    plt.yticks(np.arange(mediana.min() - 2, media.max() + 1, 0.5))
    plt.xlabel('Trimestre/Año')
    plt.ylabel('Edad')
    plt.title('Evolución de Media y Mediana de Edad por Trimestre y Año')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.ylim(mediana.min() - 2, media.max() + 1)

    st.pyplot(plt)
    plt.clf()

def mostrar_distribucion_poblacional_por_grupos(df_individuos):
    """ Muestra un grafico de barras con la distribución de la poblacion por grupos de edad (de 10 en 10 años) y sexo, 
     segun el año y trimestre que el usuario elija.  """

    st.markdown('<h2><u>Distribución poblacional por sexo y grupos de edad</u></h2>', unsafe_allow_html=True)
    
    # Reemplazo valores negativos como nulos
    df_individuos['CH06'] = df_individuos['CH06'].replace(-1, pd.NA)
    # Elimino filas nulas
    df_individuos = df_individuos.dropna(subset=['CH06'])

    # Obtengo los anos disponibles, ordenados
    anios_disponibles = sorted(df_individuos['ANO4'].dropna().unique())

    # Elijo el año (solo los que existen)
    anio = st.selectbox("Elegí el año:", anios_disponibles)

    # Para ese año, muestro solo los trimestres que existen
    trimestres_disponibles = sorted(df_individuos[df_individuos['ANO4'] == anio]['TRIMESTRE'].unique())
    trimestre = st.selectbox("Elegí el trimestre:", trimestres_disponibles)
    df_filtrado = df_individuos[(df_individuos.ANO4 == anio) & (df_individuos.TRIMESTRE == trimestre)]

    # Agrupo edades en grupos de 10 años
    bins = list(range(0, 100, 10)) + [float('inf')]
    labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']

    # Filtro las edades del dataframe segun su grupo
    df_filtrado['grupo_edad'] = pd.cut(df_filtrado['CH06'], bins=bins, labels=labels, right=False)

    # Agrupo y sumo la poblacion de acuerdo a la ponderacion
    resultado = df_filtrado.groupby(['grupo_edad', 'CH04_str'])['PONDERA'].sum().reset_index()

    # Pivot para tener una columna por sexo
    pivot = resultado.pivot(index='grupo_edad', columns='CH04_str', values='PONDERA')

    # Grafico
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind='bar', ax=ax)
    plt.xticks(rotation=0)
    ax.set_title(f'Distribucion de poblacion por grupo de edad y sexo\nAño: {anio}, Trimestre: {trimestre}')
    ax.set_xlabel('Grupo de edad')
    ax.set_ylabel('Poblacion')
    ax.legend(title='Sexo')
    st.pyplot(fig)

def mostrar_dependencia_demografica(df_individuos, df_aglomerados):
    """ Muestra como cambia la dependencia demografica a lo largo del tiempo en un aglomerado seleccionado. """
    
    st.markdown('<h2><u>Evolución de la dependencia demográfica por aglomerado</u></h2>', unsafe_allow_html=True)

    # Reemplazo valores negativos como nulos
    df_individuos['CH06'] = df_individuos['CH06'].replace(-1, pd.NA)
    # elimino filas nulas
    df_individuos = df_individuos.dropna(subset=['CH06'])

     # Selector por nombre de aglomerado
    nombres_aglomerados = df_aglomerados['nombre'].sort_values().tolist()
    nombre_elegido = st.selectbox("Elegí un aglomerado:", nombres_aglomerados)

    df_resultado = calcular_dependencia_demografica(df_individuos, df_aglomerados, nombre_elegido)

    # Mostrar gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_resultado['Periodo'], df_resultado['Dependencia'], marker='o')
    ax.set_title(f'Evolucion de la dependencia demográfica\nAglomerado {nombre_elegido}')
    ax.set_xlabel('Periodo')
    ax.set_ylabel('Indice de Dependencia (%)')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

if __name__ == "__main__":
     st.title('Caracteristicas Demográficas')
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
          mostrar_distribucion_poblacional_por_grupos(df_individuos)
          mostrar_promedio(df_individuos,df_coordenadas)
          mostrar_dependencia_demografica(df_individuos, df_coordenadas)
          mostrar_media_y_mediana(df_individuos)
          