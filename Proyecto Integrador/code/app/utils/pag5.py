import pandas as pd

def calcular_porcentajes_de_empleo(df_individuos):
    # FILTRO LOS QUE TIENEN OCUPACION Y ME FIJO QUE OCUPACION PRINCIPAL TIENEN
    df_ocupados = df_individuos[df_individuos['CONDICION_LABORAL'].str.lower().str.contains('ocupado')]
    df_ocupados = df_ocupados[df_ocupados['PP04A'].isin([1, 2, 3])]

    # LOS AGRUPO POR AGLOMERADO Y TIPO DE EMPLEO (PP04A), PONDERADO
    grupo = df_ocupados.groupby(['AGLOMERADO', 'PP04A'])['PONDERA'].sum().unstack(fill_value=0)

    # MODIFICO NOMBRE DE COLUMNAS Y CREO UNA NUEVA CON LA SUMA DEL TOTAL DE OCUPADOS SIN IMPORTAR EMPLEO
    grupo.columns = ['Empleo estatal', 'Empleo privado', 'Otro tipo']
    grupo['Total ocupados'] = grupo.sum(axis=1)

    # CALCULO PORCENTAJE DE CADA UNO
    grupo['Estatal'] = (grupo['Empleo estatal'] / grupo['Total ocupados']) * 100
    grupo['Privado'] = (grupo['Empleo privado'] / grupo['Total ocupados']) * 100
    grupo['Otro tipo'] = (grupo['Otro tipo'] / grupo['Total ocupados']) * 100

    resultado = grupo[['Total ocupados', 'Estatal', 'Privado', 'Otro tipo']].round(2)

    return resultado

def calcular_tasa_laboral(df, tipo='empleo'):
    """ Calcula la tasa de empleo o desempleo para un DataFrame filtrado por aglomerado y período."""

    df['CONDICION_LABORAL'] = df['CONDICION_LABORAL'].str.lower()
    ocupados = df[df['CONDICION_LABORAL'].isin(['ocupado dependiente', 'ocupado autonomo'])]['PONDERA'].sum()
    desocupados = df[df['CONDICION_LABORAL'] == 'desocupado']['PONDERA'].sum()
    total = ocupados + desocupados

    if total == 0:
        return None

    return (ocupados / total) * 100 if tipo == 'empleo' else (desocupados / total) * 100

def calcular_evolucion_empleo_y_desempleo(df_individuos,df_aglomerados):
    # Armo columna año/trimestre
    df_individuos['Anio/Trim'] = df_individuos['ANO4'].astype(str) + '/' + df_individuos['TRIMESTRE'].astype(str)

    # Obtengo todos los periodos, ordenados
    periodos = sorted(df_individuos['Anio/Trim'].unique())

    tasas_empleo = []
    tasas_desempleo = []

    # Calculo las tasas para cada periodo usando funciones auxiliares
    for periodo in periodos:
        df_periodo = df_individuos[df_individuos['Anio/Trim'] == periodo]
        tasas_empleo.append(calcular_tasa_laboral(df_periodo))
        tasas_desempleo.append(calcular_tasa_laboral(df_periodo, 'desempleo'))
    
    # Creo nuevo DataFrame para graficar
    df_tasas = pd.DataFrame({
        'Anio/Trim': periodos,
        'Tasa de empleo': tasas_empleo,
        'Tasa de desempleo': tasas_desempleo
    })

    return df_tasas

def calcular_desocupados_segun_educacion(df, anio, trimestre):
     # Filtro el dataframe segun ese anio y trimestress
    df_filtrado = df[(df.ANO4 == anio) & (df.TRIMESTRE == trimestre)]

     # Quito espacios y paso a minuscula el valor de condicion laboral
    df_filtrado['CONDICION_LABORAL'] = df_filtrado['CONDICION_LABORAL'].str.strip().str.lower()

    #Filtro las personas desocupadas de ese anio y trimestre
    df_desocupados = df_filtrado[df_filtrado['CONDICION_LABORAL'] == 'desocupado']
    educacion_serie = df_desocupados.groupby('NIVEL_ED_str')['PONDERA'].sum().sort_values(ascending=False)

    return educacion_serie