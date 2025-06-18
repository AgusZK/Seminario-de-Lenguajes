from pathlib import Path
import streamlit as st
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(str(Path(__file__).resolve().parents[2]))
from pipeline.rutas import PROCESADOS_PATH

def mostrar_promedio(individuos):
    """ Recibe el DF por parametro y muestra en un grafico de barras el promedio de edad del ultimo trimestre del ultimo año registrado, calculandolo"""
    
    # ME GUARDO ULTIMO ANIO Y TRIM
    ultimo_anio = individuos['ANO4'].max()
    ultimo_trim = individuos[individuos["ANO4"] == ultimo_anio]["TRIMESTRE"].max()

    st.markdown("<h2><u>Promedio de edades</u></h2>", unsafe_allow_html=True)
    st.info(f'Ultimo año y trimestre registrado: 0{ultimo_trim}/{ultimo_anio}')

    # FILTRO LAS PERSONAS DEL ULTIMO TRIM DEL ULTIMO ANIO
    datos_filtrados = individuos[(individuos["ANO4"] == ultimo_anio) & (individuos["TRIMESTRE"] == ultimo_trim)]

    # CALCULO EDAD PROMEDIO ORDENADA POR AGLOMERADO, REDONDEO EN 2 DECIMALES
    # TE QUEDA FILTRADO EN UN SERIES (AGLOMERADO -> PROMEDIO DE EDAD PONDERADO)
    # APLICO FUNCION PARA MULTIPLICAR (EDAD * CANT EN PONDERA) / SUMA DE PONDERA / TAMBIEN SE PUEDE CREAR NUEVA COLUMNA SOLO EN EL DF
    # RESET_INDEX CH6 PARA ASIGNAR NOMBRE A LA NUEVA COLUMNA QUE TIENE LOS VALORES PONDERADOS, APPLY LE SACA EL NOMBRE
    edad_promedio = (datos_filtrados.groupby("AGLOMERADO")
                     .apply(lambda df: (df["CH06"] * df["PONDERA"]).sum() / df["PONDERA"].sum())
                     .round(2)
                     .reset_index(name="CH06")
                     )

    # GRAFICO
    agloms = edad_promedio["AGLOMERADO"]
    agloms = agloms.astype(str) # LO PASO A STR PARA QUE NO CALCULE UN RANGO MUY GRANDE Y QUEDEN ESPACIOS VACIOS
    edades = edad_promedio["CH06"]
    max_edad = edades.max()
    min_edad = edades.min()

    plt.figure(figsize=(10,6))
    plt.bar(agloms, edades, width=0.4, color='skyblue')
    plt.title('Edad promedio por Aglomerado')
    plt.xlabel('Aglomerado')
    plt.ylabel('Edad promedio')
    plt.ylim(min_edad - 1, max_edad + 1)
    plt.yticks(np.arange(np.floor(min_edad - 1), np.ceil(max_edad ) + 1, 1))
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()

    st.pyplot(plt)
    plt.clf()

def calcular_mediana_ponderada (df):
    """ Calcula especificamente la mediana ponderada, quedandose con el primer valor mayor-igual a la mitad"""  
    
    # ORDENA DE MENOR A MAYOR EDAD PARA BUSCAR EL VALOR DEL MEDIO
    df = df.sort_values('CH06')
    # SUMA CANTIDAD TOTAL DE PONDERA Y CALCULA LA MITAD
    total_pondera = df['PONDERA'].sum()
    mitad = total_pondera / 2
    # CREA NUEVA COLUMNA CON LA SUMA ACUMULATIVA DE PONDERA
    df['acum_pondera'] = df['PONDERA'].cumsum()
    # BUSCA LAS FILAS DONDE ESA ACUMULACION ES MAYOR O IGUAL A LA MITAD
    # UNA VEZ ENCUENTRA LA FILA, SE QUEDA CON EL PRIMERO QUE ES MAYOR-IGUAL
    mediana_row = df[df['acum_pondera'] >= mitad].iloc[0]

    # DEVUELVE EL VALOR ENCONTRADO, QUE SERIA LA MEDIANA
    return mediana_row['CH06']

def calcular_media_mediana(df):
    """ Calcula por separado la media y la mediana a partir del DF y las retorna en un series ambas, redondeando el resultado"""    
    
    # SUMA LOS VALORES DE LA COLUMNA EDAD PONDERADA DEL ANIO/TRIM Y LOS DIVIDE POR EL TOTAL DE PONDERA
    media = df['edad_ponderada'].sum() / df['PONDERA'].sum()
    # APLICA FUNCION PARA BUSCAR MEDIANA
    mediana = calcular_mediana_ponderada(df)

    return pd.Series({'MEDIA': round(media, 2), 'MEDIANA': round(mediana,2)})

def mostrar_media_y_mediana (individuos):
    """ Recibe el DF por parametro y muestra la evolucion de la media y mediana en un grafico de lineas"""
    
    st.markdown("<h2><u>Media y Mediana de edades</u></h2>", unsafe_allow_html=True)
    # CREO COLUMNA EN EL DF CON LA EDAD PONDERADA
    individuos['edad_ponderada'] = individuos['CH06'] * individuos['PONDERA']

    # APLICA UN SOLO APPLY:
    #   CALCULA LA MEDIA Y MEDIANA POR ANIO/TRIM
    #   LAS RETORNA EN UN SERIES COMO NUEVAS COLUMNAS
    media_mediana = individuos.groupby(['ANO4', 'TRIMESTRE']).apply(calcular_media_mediana).reset_index()

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
    bins = list(range(0, 120, 10)) 
    labels = ['0-9', '10-19', '20-29', '30-39', '40-49','50-59','60-69','70-79','80-89', '90-99', '100-119']

    # Filtro las edades del dataframe segun su grupo
    df_filtrado['grupo_edad'] = pd.cut(df_filtrado['CH06'], bins=bins, labels=labels, right=False)

    # Agrupo y sumo la poblacion de acuerdo a la ponderacion
    resultado = df_filtrado.groupby(['grupo_edad', 'CH04_str'])['PONDERA'].sum().reset_index()

    # Pivot para tener una columna por sexo
    pivot = resultado.pivot(index='grupo_edad', columns='CH04_str', values='PONDERA')

    # Grafico
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    ax.set_title(f'Distribucion de poblacion por grupo de edad y sexo\nAño: {anio}, Trimestre: {trimestre}')
    ax.set_xlabel('Grupo de edad')
    ax.set_ylabel('Poblacion')
    ax.legend(title='Sexo')
    st.pyplot(fig)

def mostrar_dependencia_demografica(df_individuos):
    st.markdown('<h2><u>Evolución de la dependencia demográfica por aglomerado</u></h2>', unsafe_allow_html=True)

    # Reemplazo valores negativos como nulos
    df_individuos['CH06'] = df_individuos['CH06'].replace(-1, pd.NA)
    # elimino filas nulas
    df_individuos = df_individuos.dropna(subset=['CH06'])

    # muestro aglomerados disponibles de manera ordenada
    aglomerados_disponibles = sorted(df_individuos['AGLOMERADO'].dropna().unique())
    aglomerado = st.selectbox("Elegí un aglomerado:", aglomerados_disponibles)

    # filtro el DataFrame por el aglomerado elegido
    df_aglo = df_individuos[df_individuos['AGLOMERADO'] == aglomerado]

    # creo una columna de periodo para agrupar ej: 2023-T1
    df_aglo['PERIODO'] = df_aglo['ANO4'].astype(str) + '-T' + df_aglo['TRIMESTRE'].astype(str)

    # almacenara los resultados de dependencia de cada periodo
    resultados_dependencia = []

    # itera sobre cada grupo de filas correspondientes a un mismo periodo (mismo anio y trismeste)
    for periodo, grupo in df_aglo.groupby('PERIODO'):
        menores = grupo[(grupo['CH06'] <= 14) | (grupo['CH06'] >= 65)]['PONDERA'].sum()
        activos = grupo[(grupo['CH06'] >= 15) & (grupo['CH06'] <= 64)]['PONDERA'].sum()

        if activos > 0:
            dependencia = (menores / activos) * 100
        else:
            dependencia = None

        resultados_dependencia.append({'Periodo': periodo, 'Dependencia': dependencia})

    # convierto en DataFrame la lista de resultados, ordenado segun el periodo
    df_resultado = pd.DataFrame(resultados_dependencia).sort_values(by='Periodo')

    # Mostrar gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_resultado['Periodo'], df_resultado['Dependencia'], marker='o')
    ax.set_title(f'Evolucion de la dependencia demográfica\nAglomerado {aglomerado}')
    ax.set_xlabel('Periodo')
    ax.set_ylabel('Indice de Dependencia (%)')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

if __name__ == "__main__":
     st.title('Caracteristicas Geograficas')
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
          mostrar_promedio(df_individuos)
          mostrar_media_y_mediana(df_individuos)
          mostrar_distribucion_poblacional_por_grupos(df_individuos)
          mostrar_dependencia_demografica(df_individuos)
          