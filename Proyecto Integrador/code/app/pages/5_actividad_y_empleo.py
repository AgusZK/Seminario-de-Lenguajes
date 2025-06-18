from pathlib import Path
import streamlit as st
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
sys.path.append(str(Path(__file__).resolve().parents[2]))
from pipeline.rutas import PROCESADOS_PATH, AGLOMERADOS_COORDENADAS


def mostrar_evolucion_empleo_y_desempleo(df_individuos):
    """ Recibe el DF por parametro y muestra en un grafico de lineas la tasa de empleo y desempleo respectivamente en un aglomerado seleccionado, en caso de no elegir lo muestra en todo el pais""" 
    
    st.markdown("<h2><u>Evolución del empleo y desempleo</u></h2>", unsafe_allow_html=True)
    # Armo columna año/trimestre
    df_individuos['Anio/Trim'] = df_individuos['ANO4'].astype(str) + '/' + df_individuos['TRIMESTRE'].astype(str)
    df_individuos['CONDICION_LABORAL'] = df_individuos['CONDICION_LABORAL'].str.lower()

    # Filtro condiciones validas
    condiciones_validas = ['ocupado dependiente', 'ocupado autonomo', 'desocupado']
    df_valido = df_individuos[df_individuos['CONDICION_LABORAL'].isin(condiciones_validas)]

    # Selector de aglomerado
    agloms_disponibles = sorted(df_valido['AGLOMERADO'].dropna().unique())
    aglom_elegido = st.selectbox('Filtrar por aglomerado', ['Todo el país'] + list(agloms_disponibles), index=0)

    if aglom_elegido != 'Todo el país':
        df_valido = df_valido[df_valido['AGLOMERADO'] == aglom_elegido]

    # Agrupo por periodo y condicion
    grupo = df_valido.groupby(['Anio/Trim', 'CONDICION_LABORAL']).size().unstack(fill_value=0)
    
    # Calculo de porcentajes
    grupo['Tasa de empleo'] = grupo.apply(
        lambda row: (row.get('ocupado dependiente', 0) +
                     row.get('ocupado autonomo', 0)) / 
                    (row.get('ocupado dependiente', 0) +
                     row.get('ocupado autonomo', 0) +
                     row.get('desocupado', 0)) * 100,
        axis=1)

    grupo['Tasa de desempleo'] = grupo.apply(
        lambda row: row.get('desocupado', 0) / 
                    (row.get('ocupado dependiente', 0) +
                     row.get('ocupado autonomo', 0) +
                     row.get('desocupado', 0)) * 100,
        axis=1)

    grupo_ordenado = grupo.sort_index().reset_index()

    # Creo titulos para el grafico
    titulo_desemp = "Tasa de Desempleo "
    titulo_empleo = "Tasa de Empleo "
    if aglom_elegido == "Todo el país":
        titulo_desemp += "(todo el país)"
        titulo_empleo += "(todo el país)"
    else:
        titulo_desemp += f"(aglomerado {aglom_elegido})"
        titulo_empleo += f"(aglomerado {aglom_elegido})"

    # Creo figura con dos subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

    # Grafico de tasa de desempleo
    axes[0].plot(grupo_ordenado['Anio/Trim'], grupo_ordenado['Tasa de desempleo'], marker='o', color='red')
    axes[0].set_title(titulo_desemp)
    axes[0].set_xlabel('Año/Trimestre')
    axes[0].set_ylabel('%')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True)

    # Grafico de tasa de empleo
    axes[1].plot(grupo_ordenado['Anio/Trim'], grupo_ordenado['Tasa de empleo'], marker='o', color='green')
    axes[1].set_title(titulo_empleo)
    axes[1].set_xlabel('Año/Trimestre')
    axes[1].set_ylabel('%')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True)

    st.pyplot(fig)
    plt.clf()


def mostrar_porcentajes_de_empleo(df_individuos):
    """ Recibe el DF por parametro y muestra en un grafico de barras agrupadas el porcentaje de los diferentes tipos de empleo registrados""" 
    
    st.markdown("<h2><u>Porcentaje de empleo estatal/privado/otros</u></h2>", unsafe_allow_html=True)
    # FILTRO LOS QUE TIENEN OCUPACION Y ME FIJO QUE OCUPACION PRINCIPAL TIENEN
    df_ocupados = df_individuos[df_individuos['CONDICION_LABORAL'].str.lower().str.contains('ocupado')]
    df_ocupados = df_ocupados[df_ocupados['PP04A'].isin([1, 2, 3])]

    # LOS AGRUPO POR AGLOMERADO, OCUPACION
    grupo = df_ocupados.groupby(['AGLOMERADO', 'PP04A']).size().unstack(fill_value=0)

    # MODIFICO NOMBRE DE COLUMNAS Y CREO UNA NUEVA CON LA SUMA DEL TOTAL DE OCUPADOS SIN IMPORTAR EMPLEO
    grupo.columns = ['Empleo estatal', 'Empleo privado', 'Otro tipo']
    grupo['Total ocupados'] = grupo.sum(axis=1)

    # CALCULO PORCENTAJE DE CADA UNO
    grupo['% Estatal'] = (grupo['Empleo estatal'] / grupo['Total ocupados']) * 100
    grupo['% Privado'] = (grupo['Empleo privado'] / grupo['Total ocupados']) * 100
    grupo['% Otro tipo'] = (grupo['Otro tipo'] / grupo['Total ocupados']) * 100

    resultado = grupo[['Total ocupados', '% Estatal', '% Privado', '% Otro tipo']].round(2)

    # GRAFICO
    resultado[['% Estatal', '% Privado', '% Otro tipo']].plot(
        kind='bar',
        figsize=(12, 6),
        colormap='Set1'
    )
    plt.title('Porcentaje de tipo de empleo por aglomerado')
    plt.ylabel('Porcentaje')
    plt.xlabel('Aglomerado')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(np.arange(0, 101, 5))
    plt.legend(title='Tipo de empleo')
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()

    st.pyplot(plt)
    plt.clf()

def mostrar_desocupados_segun_educacion(df_individuos):
    st.markdown("<h2><u>Distribucion de personas desocupadas segun su nivel educativo</u></h2>", unsafe_allow_html=True)

    # Obtengo los anos disponibles, ordenados
    anios_disponibles = sorted(df_individuos['ANO4'].dropna().unique())

    # Elijo el año (solo los que existen)
    anio = st.selectbox("Elegí el año:", anios_disponibles)

    # Para ese año, muestro solo los trimestres que existen
    trimestres_disponibles = sorted(df_individuos[df_individuos['ANO4'] == anio]['TRIMESTRE'].unique())
    trimestre = st.selectbox("Elegí el trimestre:", trimestres_disponibles)

    # Filtro el dataframe segun ese anio y trimestre
    df_filtrado = df_individuos[(df_individuos.ANO4 == anio) & (df_individuos.TRIMESTRE == trimestre)]

    # Quito espacios y paso a minuscula el valor de condicion laboral
    df_filtrado['CONDICION_LABORAL'] = df_filtrado['CONDICION_LABORAL'].str.strip().str.lower()

    #Filtro las personas desocupadas de ese anio y trimestre
    df_desocupados = df_filtrado[df_filtrado['CONDICION_LABORAL'] == 'desocupado']
    educacion_serie = df_desocupados.groupby('NIVEL_ED_str')['PONDERA'].sum()

    # Creo el grafico de torta
    fig, ax = plt.subplots()
    ax.pie(educacion_serie, labels=educacion_serie.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Para que sea un circulo

    ax.set_title(f'Distribucion de personas desocupadas segun nivel educativo\nAño: {anio}, Trimestre: {trimestre}')
    st.pyplot(fig)
    plt.clf()

if __name__ == "__main__":
     st.title('Actividad y Empleo')
     file = PROCESADOS_PATH/'individuos.csv'
     try:
         df_individuos = pd.read_csv(file, sep=';', low_memory=False)
     except FileNotFoundError as e:  
           st.error(f'No se ha encontrado el archivo {e.filename} para realizar las consultas')
     except UnicodeDecodeError as e:
         st.error(f'Ha ocurrido un error de formato al intentar leer el archivo {e}')
     except Exception as e:
         print(f'Ocurrio un error inesperado: {e}')
     else:
        mostrar_evolucion_empleo_y_desempleo(df_individuos)
        mostrar_porcentajes_de_empleo(df_individuos)
        mostrar_desocupados_segun_educacion(df_individuos)