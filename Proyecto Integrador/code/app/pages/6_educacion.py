from pathlib import Path
import streamlit as st
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
import matplotlib.pyplot as plt

from pipeline.consultas import informar_rankings
from pipeline.rutas import PROCESADOS_PATH

st.set_page_config(
    page_title="Educacion",
)
st.markdown(
    """
    ## Pagina en donde se muestras datos relacionados con la educacion
    """
)
NIVEL ="NIVEL_ED_str"
EDAD = "CH06"
PONDERA = "PONDERA"

df_original = pd.read_csv(PROCESADOS_PATH/"individuos.csv", sep=";", low_memory=False)

def cantidad_por_nivel_educativo():
    """Segun un año ingresado por el usuario muestra un grafico con la cantidad de gente
    que completo el nivel de educacion"""

    st.markdown("## Torta grafica sobre la cantidad que se quedaron en un nivel educativo durante")

    if(not df_original.empty):
     
        anio = st.selectbox("Escoga un año para ver la cantidad de gente que se quedo en un nivel educativo", sorted(df_original["ANO4"].unique()) )
        

        anio_buscado = df_original[df_original["ANO4"] == anio].copy()
        niveles_educativos = ["Primario completo","Secundario completo","Superior o universitario"]
        anio_buscado = anio_buscado[anio_buscado[NIVEL].isin(niveles_educativos)]   
        anio_buscado = anio_buscado.groupby(NIVEL)[PONDERA].sum().reset_index()
        #Grafico
        etiquetas_edu = anio_buscado[NIVEL]
        valores = anio_buscado[PONDERA]
        aux = []
        for nivel, valor in zip(etiquetas_edu,valores):
            aux.append((f"{nivel} : ({valor})")) 

        fig, ax = plt.subplots(figsize =(8,8))
        ax.pie(valores,labels = etiquetas_edu, colors= ["orange","blue","red"])
        ax.set_title(f"Proporcion de personas por nivel de educacion durante el año: {anio}")
        ax.legend(aux, loc="upper right", bbox_to_anchor =(1.2,1.0))
        st.pyplot(fig)
        st.warning("No se encuentra dicho año en la base de datos")

def mostrar_nivel_alcanzado():  
    """ Muestra un grafico de los con los niveles de educacion que llegaron las personas
    en cierta edad  """

    copia = df_original.copy()

    #Creo lista de elementos que me interesan guardar
    niveles_educativos = ["Primario completo","Secundario completo","Superior o universitario"]
    #Me guardo en la copia del data unicamente los niveles que busco
    copia = copia[copia[NIVEL].isin(niveles_educativos)]
    
    entre20_y30 = copia[copia[EDAD].between(20,29)]
    entre30_y40 = copia[copia[EDAD].between(30,39)]
    entre40_y50 = copia[copia[EDAD].between(40,49)]
    entre50_y60 = copia[copia[EDAD].between(50,59)]
    mayores_60 = copia[copia[EDAD]>= 60]
    
    #Acumulo segun el nivel educativo y la ponderacion
    mas20 = entre20_y30.groupby(NIVEL)[PONDERA].sum().reset_index()
    mas30 = entre30_y40.groupby(NIVEL)[PONDERA].sum().reset_index()
    mas40 = entre40_y50.groupby(NIVEL)[PONDERA].sum().reset_index()
    mas50 = entre50_y60.groupby(NIVEL)[PONDERA].sum().reset_index()
    mas_60 = mayores_60.groupby(NIVEL)[PONDERA].sum().reset_index()
    
    datos_disponibles = {
        "Entre 20 y 30" : mas20,
        "Entre 30 y 40": mas30,
        "Entre 40 y 50": mas40,
        "Entre 50 y 60": mas50,
        "Mas de 60 ": mas_60
    }
    st.markdown("## Nivel educativo mas comun alcanzo segun algunos grupos etarios ")

    st.write("Marque los intervalos que le gustaria graficar")
    seleccion = []
    botones = list(datos_disponibles.keys())
    #almaceno los botones que quiere ver el usuario
    for boton in botones:
        if(st.checkbox(boton)):
            seleccion.append(boton)
    
    #Busco el id maximo y lo añado a mi serie
    series = []
    for dato in sorted(seleccion):
        aux = datos_disponibles[dato]
        maximo = aux[PONDERA].idxmax()
        aux["Rango de edad"] = dato
        series.append(aux.loc[maximo]) 
      

    df_a_mostrar = pd.DataFrame(series)
    

    if(not df_a_mostrar.empty):
        df_a_mostrar["Info"] = df_a_mostrar["Rango de edad"] + "\n" + df_a_mostrar[NIVEL]
        fig, ax = plt.subplots(figsize=(12, 5))
        df_a_mostrar.plot(kind= "bar", x= "Info", y = PONDERA, ax=ax, legend=False,color="green",width= 0.3)
    
        ax.set_title('Grafico sobre el nivel mas comun por grupos etario seleccionados')
        plt.xticks(rotation=0)
        ax.set_xlabel("## Rango de edades")
        ax.set_ylabel("Cantidad de personas")
        st.pyplot(fig)
 


def exportar_ranking_aglomerado():
    """Permite exportar un archivo de rankings si se presiona el boton, se guarda en la carpeta de procesados"""
    st.markdown("Presione el boton para generar un archivo csv para su exportacion sobre los rankings de aglomerados")
    
    rankings =pd.DataFrame(informar_rankings()) 
    if(not rankings.empty):
        st.dataframe(rankings)
        st.download_button(
            label="Exportar ranking de aglomerados",
            data=rankings.to_csv(sep=";", index=False).encode('utf-8'),
            file_name='ranking_aglomerados.csv',
            mime='text/csv',)
    else:
        st.warning("Ha ocurrido un error")


            

def informar_alfabetizados():
    """Muestra un grafico con los porcentajes de la gente que sabe leer y escribir, y los que no por año"""

    leer = "CH09"
    #Creo una copia para no trabajar con el original
    copia = df_original.copy()
    #Transformo las columnas a enteros
    copia[EDAD] = copia[EDAD].astype(int)
    copia[leer] = copia[leer].astype(int)

    #Filtro para quedarme unicamente los valores de si saben leer o no
    copia = copia[copia[leer] != 9]
    conjunto= copia[copia[EDAD] > 6].groupby(["ANO4",leer])[PONDERA].sum()
    datos = pd.DataFrame(conjunto.reset_index())

    #Calculo los porcentajes segun por año y los agrego a una nueva columna en datos
    for anio in datos["ANO4"].unique():
        si_leen = datos[(datos["ANO4"] == anio) & (datos[leer] == 1)][PONDERA].sum()
        no_leen = datos[(datos["ANO4"] == anio) & (datos[leer] == 2)][PONDERA].sum()
        total = si_leen + no_leen
        porc_leen = round(si_leen/total * 100,2)
        porc_no_leen = round(no_leen/total*100,2)
        #Para el año actual y segun si sabe leer o escribir, implemento una columna "porcentaje" con dicho porcentaje 
        datos.loc[(datos["ANO4"] == anio) & (datos[leer] == 1), "porcentaje"] = porc_leen
        datos.loc[(datos["ANO4"] == anio) & (datos[leer] == 2), "porcentaje"] = porc_no_leen

    st.markdown("## Grafico sobre los porcentajes de alfabetizacion durante los años")

    #Pivot para organizar los porcentajes de quienes saben leer y quien no
    pivot = datos.pivot(index="ANO4", columns=leer, values="porcentaje")
    #representacio de cada columna
    pivot.columns = ["Sabe leer","No sabe leer",""]


    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind='bar', ax=ax,width = 0.4)
    plt.xticks(rotation=0)
    #añado a cada columna su porcentaje 
    for i, anio in enumerate(pivot.index):
        for j, col in enumerate(pivot.columns):
            valor = pivot.loc[anio, col]
            ax.annotate(f'{valor:.1f}%',
                        xy=(i + j * 0.2 - 0.1, valor + 0.5),
                        fontsize=9)
    ax.set_title('Porcentaje de gente alfabetizadas por año')
    ax.set_xlabel('Años')
    
    ax.set_ylabel('Porcentaje')
    ax.legend(title='Condición',loc= "upper right",bbox_to_anchor = (1.2,1.0))
    st.pyplot(fig)

cantidad_por_nivel_educativo()
mostrar_nivel_alcanzado()
informar_alfabetizados()
exportar_ranking_aglomerado()