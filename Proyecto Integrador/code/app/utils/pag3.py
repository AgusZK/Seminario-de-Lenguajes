import pandas as pd

def calcular_promedio(individuos, df_aglomerados):
    # ME GUARDO ULTIMO ANIO Y TRIM
    ultimo_anio = individuos['ANO4'].max()
    ultimo_trim = individuos[individuos["ANO4"] == ultimo_anio]["TRIMESTRE"].max()

    # FILTRO LAS PERSONAS DEL ULTIMO TRIM DEL ULTIMO ANIO
    datos_filtrados = individuos[(individuos["ANO4"] == ultimo_anio) & (individuos["TRIMESTRE"] == ultimo_trim)]

    # CALCULO EDAD PROMEDIO ORDENADA POR AGLOMERADO, REDONDEO EN 2 DECIMALES
    edad_promedio = (datos_filtrados.groupby("AGLOMERADO")
                     .apply(lambda df: (df["CH06"] * df["PONDERA"]).sum() / df["PONDERA"].sum())
                     .round(2)
                     .reset_index(name="Edad promedio")
                     )

    # GRAFICO
    # USO EL NUM DEL AGLOMERADO EN MI DF PARA BUSCARLO EN EL DF DE AGLOMERADOS PARA OBTENER EL NOMBRE, LO MERGEO Y CREO COLUMNA NUEVA 'NOMBRE'
    edad_promedio = edad_promedio.merge(df_aglomerados[['aglomerado', 'nombre']], left_on='AGLOMERADO', right_on='aglomerado', how='left')
    edad_promedio['AGLOMERADO'] = edad_promedio['AGLOMERADO'].astype(str)

    return edad_promedio

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
    """ Calcula por separado la media y la mediana a partir del DataFrame y las retorna en un series ambas, redondeando el resultado"""    
    
    # SUMA LOS VALORES DE LA COLUMNA EDAD PONDERADA DEL ANIO/TRIM Y LOS DIVIDE POR EL TOTAL DE PONDERA
    media = df['edad_ponderada'].sum() / df['PONDERA'].sum()
    # APLICA FUNCION PARA BUSCAR MEDIANA
    mediana = calcular_mediana_ponderada(df)

    return pd.Series({'MEDIA': round(media, 2), 'MEDIANA': round(mediana,2)})

def calcular_media_y_mediana(individuos):
    # CREO COLUMNA EN EL DF CON LA EDAD PONDERADA
    individuos['edad_ponderada'] = individuos['CH06'] * individuos['PONDERA']

    # APLICA UN SOLO APPLY:
    #   CALCULA LA MEDIA Y MEDIANA POR ANIO/TRIM
    #   LAS RETORNA EN UN SERIES COMO NUEVAS COLUMNAS
    media_mediana = individuos.groupby(['ANO4', 'TRIMESTRE']).apply(calcular_media_mediana).reset_index()

    return media_mediana

def calcular_dependencia_demografica(df, df_aglomerados, nombre_elegido):
    # Reemplazo valores negativos como nulos
    df['CH06'] = df['CH06'].replace(-1, pd.NA)
    # elimino filas nulas
    df = df.dropna(subset=['CH06'])

    # Obtener ID del aglomerado
    aglomerado_id = df_aglomerados[df_aglomerados['nombre'] == nombre_elegido]['aglomerado'].values[0]

    # Filtrar DataFrame por aglomerado
    df_aglo = df[df['AGLOMERADO'] == aglomerado_id]

    # creo una columna de periodo para agrupar ej: 2023-T1
    df_aglo['PERIODO'] = df_aglo['ANO4'].astype(str) + '-T' + df_aglo['TRIMESTRE'].astype(str)

    # almacenara los resultados de dependencia de cada periodo
    resultados_dependencia = []

    # itera sobre cada grupo de filas correspondientes a un mismo periodo (mismo anio y trismeste)
    for periodo, grupo in df_aglo.groupby('PERIODO'):
        dependientes = grupo[(grupo['CH06'] <= 14) | (grupo['CH06'] >= 65)]['PONDERA'].sum()
        activos = grupo[(grupo['CH06'] >= 15) & (grupo['CH06'] <= 64)]['PONDERA'].sum()

        if activos > 0:
            dependencia = (dependientes / activos) * 100
        else:
            dependencia = None

        resultados_dependencia.append({'Periodo': periodo, 'Dependencia': dependencia})

    # convierto en DataFrame la lista de resultados, ordenado segun el periodo
    return pd.DataFrame(resultados_dependencia).sort_values(by='Periodo')