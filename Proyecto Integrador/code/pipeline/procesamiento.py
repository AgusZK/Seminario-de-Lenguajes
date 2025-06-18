import os
import csv
from pipeline.rutas import INDIVIDUOS_PATH, HOGARES_PATH, PROCESADOS_PATH

# ------------- FUNCIONES GENERALES INDIVIDUOS ------------------

def agregar_CH04 (row):
    """ Traduce 1 y 2 a Varon y Mujer en nueva columna respectivamente """
    
    genero = int(row['CH04'])

    if genero == 1:
        row['CH04_str'] = 'Varon'
    else:
       row['CH04_str'] = 'Mujer'
    return row

def agregar_nivel_ED(row):
    """ Traduce valores numericos a una nueva columna en cadena """

    nivel_educativo = int(row['NIVEL_ED'])

    if nivel_educativo == 1:
        row['NIVEL_ED_str'] = 'Primario incompleto'

    elif nivel_educativo == 2:
        row['NIVEL_ED_str']= 'Primario completo'

    elif nivel_educativo == 3:
        row['NIVEL_ED_str'] = 'Secundario incompleto'   
         
    elif nivel_educativo == 4:
        row['NIVEL_ED_str'] = 'Secundario completo'    
        
    elif nivel_educativo in [5,6]: 
        row['NIVEL_ED_str'] = 'Superior o universitario'
        
    elif nivel_educativo in [7,9]: 
         row['NIVEL_ED_str'] = 'Sin informacion'

    return row

def agregar_condicion_laboral(row):
    """ Dependiendo la condicion laboral se traduce en una nueva columna """

    valor_estado = int(row['ESTADO'])
    valor_categoria = int(row['CAT_OCUP'])

    if valor_estado == 1 and valor_categoria in [1, 2]:
        row['CONDICION_LABORAL'] = 'Ocupado autonomo'

    elif valor_estado == 1 and valor_categoria in [3, 4, 9]:
        row['CONDICION_LABORAL'] = 'Ocupado dependiente'

    elif valor_estado == 2:
        row['CONDICION_LABORAL'] = 'Desocupado'

    elif valor_estado == 3:
       row['CONDICION_LABORAL']  = 'Inactivo'

    else:
        row['CONDICION_LABORAL'] = 'Fuera de categoria/sin informacion'
    
    return row

def agregar_universitario(row):
    """ Revisa si es mayor de edad y si termino la universidad o no, traduciendolo a una nueva columna """

    edad = int(row['CH06'])
    nivel_educativo = int(row['NIVEL_ED'])

    if edad >= 18:
        if nivel_educativo == 6:
            row['UNIVERSITARIO'] = '1'
        else:
            row['UNIVERSITARIO'] = '0'
    else:
        row['UNIVERSITARIO'] = '2'

    return row


# ------------- FUNCIONES GENERALES HOGARES ------------------

def agregar_tipo_hogar(row):
    """ Revisa la cantidad de habitantes que tiene el hogar, traduciendolo a una nueva columna """

    habitantes = int(row['IX_TOT'])
    if habitantes == 1:
        row['TIPO_HOGAR'] = 'Unipersonal'
    elif 2 <= habitantes <= 4:
        row['TIPO_HOGAR'] = 'Nuclear'
    else:
        row['TIPO_HOGAR'] = 'Extendido'

    return row


def agregar_material_techumbre(row):
    """ Se fija el tipo de material que tiene el hogar, traduciendolo a una nueva columna """

    material = int(row['IV4'].strip())

    if 1 <= material <= 4:
        row['MATERIAL_TECHUMBRE'] = 'Material durable'
    elif 5 <= material <= 7:
        row['MATERIAL_TECHUMBRE'] = 'Material precario'
    elif material == '9':
        row['MATERIAL_TECHUMBRE'] = 'No Aplica'            

    return row

def agregar_densidad_hogar(row):
    """ Revisa columnas de total de personas y habitaciones, obtiene la densidad diviendolos y traduce el resultado
        a una nueva columna """
    
    personas = int(row['IX_TOT'])
    habitaciones = int(row['IV2'])
    densidad = personas/habitaciones

    if densidad < 1:
        row['DENSIDAD_HOGAR'] = 'Bajo'
    elif 1 <= densidad <= 2:
        row['DENSIDAD_HOGAR'] = 'Medio'
    elif densidad > 2:
        row['DENSIDAD_HOGAR'] ='Alto'
         
    return row

def agregar_condicion_habitabilidad(row):
    """ Asigna una categoria de habitabilidad (Buena, Saludable, Regular o Insuficiente)
        a una vivienda en funcion de sus condiciones basicas."""
    
    tiene_agua = row['IV6']
    origen_agua = row['IV7']
    posee_banio = row['IV8']
    techo = row['MATERIAL_TECHUMBRE']
    piso = row['IV3']

    if all(x == '1' for x in [tiene_agua, origen_agua, posee_banio, piso]) and techo == 'Material durable':
        row['CONDICION_DE_HABITABILIDAD'] = 'Buena'
    
    elif posee_banio == '1' and tiene_agua in ['1', '2'] and origen_agua in ['1', '2'] and piso in ['1', '2'] and techo == 'Material durable':
         row['CONDICION_DE_HABITABILIDAD'] = 'Saludable'

    elif posee_banio == '1' and (tiene_agua == '3' or origen_agua == '3') and piso in ['1', '2'] and techo != 'Material durable':
         row['CONDICION_DE_HABITABILIDAD'] ='Regular'

    else:
         row['CONDICION_DE_HABITABILIDAD'] ='Insuficiente'

    return row

# ------ LECTURA DE ARCHIVOS CRUDOS PARA PROCESARLOS FINALMENTE EN UN ARCHIVO .CSV ------
def unir_archivos(origen_path, salida_path):
    """Crea un archivo unificado con todos los archivos contenidos en la ruta origen
    y lo guarda en la ruta de salida"""

    # SE OBTIENEN TODOS LOS NOMBRES DE ARCHIVOS QUE HAY EN LA CARPETA ORIGEN
    archivos = os.listdir(origen_path)

    # SE UTILIZA PARA ASEGURARSE DE ESCRIBIR LOS ENCABEZADOS UNA SOLA VEZ
    encabezado_escrito = False  
    
    with open(salida_path, 'w', encoding='utf-8') as salida:
        writer = None

        # SE RECORREN TODOS LOS ARCHIVOS DE LA CARPETA ORIGEN
        for archivo in archivos:

            with open(origen_path / archivo, 'r', encoding='utf-8') as entrada:
                reader = csv.reader(entrada, delimiter=';')

                # SE OBTIENE LA PRIMERA FILA (ENCABEZADO) DEL ARCHIVO
                encabezado = next(reader)

                # SE ESCRIBE EL ENCABEZADO UNA SOLA VEZ EN EL ARCHIVO FINAL
                if not encabezado_escrito:
                    writer = csv.writer(salida, delimiter=';')
                    writer.writerow(encabezado)
                    encabezado_escrito = True

                for fila in reader:
                    writer.writerow(fila)

# ------ LECTURA DEL ARCHIVO PROCESADO, APLICACION DE FUNCIONES PARA GENERAR NUEVAS HILERAS CON INFORMACION MODIFICADA, REESCRITURA EN ARCHIVO .CSV ------
funciones_individuos = [agregar_CH04,agregar_nivel_ED,agregar_condicion_laboral,agregar_universitario]
nombres_individuos =["CH04_str","NIVEL_ED_str", "CONDICION_LABORAL","UNIVERSITARIO"]

funciones_hogares = [agregar_tipo_hogar,agregar_material_techumbre,agregar_densidad_hogar, agregar_condicion_habitabilidad]
nombres_hogares =["TIPO_HOGAR","MATERIAL_TECHUMBRE", "DENSIDAD_HOGAR", "CONDICION_DE_HABITABILIDAD"]

def reemplazar(file_path,funciones,cadenas):
    """ Obtiene el path del archivo , lista de funciones y lista de encabezados por parametros.
        Ambas listas deben coincidir en orden ya que son 1-1 
        Agrega todos los encabezados y aplica cada funcion especifica a las hileras. 
        Genera una lista de hileras con informacion modificada que luego se escribe en el archivo, modificando el original """
    
    with file_path.open('r') as file:
        reader = csv.DictReader(file, delimiter=';')
        # AGREGO TODOS LOS NUEVOS ENCABEZADOS
        fieldnames = reader.fieldnames + cadenas

        # POR CADA FILA, APLICO FUNCION DE LA LISTA DE FUNCIONES Y AGREGO EL NUEVO CONTENIDO EN FILAS_NUEVAS
        filas_nuevas = []
        for row in reader:
            for funcion in funciones:
                row = funcion(row)
            filas_nuevas.append(row)

    with file_path.open('w') as procesados_file:
        writer = csv.DictWriter(procesados_file,fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas_nuevas)

# ------ OBTENCION DE RANGO DE FECHAS PARA SABER EL PERIODO EN EL QUE NUESTRO SISTEMA TIENE INFORMACION ------        
def obtener_rango_fechas(dataset_path):
    """
    Lee el archivo CSV y obtiene el primer y último año y trimestre.

    Parámetros:
        dataset_path (str): Ruta del archivo CSV procesado.

    Retorna:
        str: Resumen del rango de fechas en el formato:
             'El sistema contiene información desde el 01/2016 hasta el 03/2024.'
    """
    primer = None
    ultimo = None

    with open(dataset_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            try:
                trimestre = int(row['TRIMESTRE'])
                anio = int(row['ANO4'])
            except (KeyError, ValueError):
                continue  # Saltar fila si faltan datos o son inválidos

            fecha = (anio, trimestre)

            if primer is None or fecha < primer:
                primer = fecha
            if ultimo is None or fecha > ultimo:
                ultimo = fecha

    if primer and ultimo:
        return f"Nuestro registro contiene información desde el trimestre {primer[1]:02}/{primer[0]} hasta el trimestre {ultimo[1]:02}/{ultimo[0]}."
    else:
        return "No se pudo determinar el rango de fechas."

# ------ LLAMADO GENERAL PARA UNIR AMBOS ARCHIVOS Y GENERARLES LAS COLUMNAS CORRESPONDIENTES, GENERALIZACION PARA EL REFRESCO EN STREAMLIT ------     
def unir_ambos_archivos ():
    unir_archivos(INDIVIDUOS_PATH, PROCESADOS_PATH / "individuos.csv")
    unir_archivos(HOGARES_PATH, PROCESADOS_PATH / "hogares.csv")

def reemplazar_ambos_archivos ():
    reemplazar(PROCESADOS_PATH / "individuos.csv", funciones_individuos, nombres_individuos)
    reemplazar(PROCESADOS_PATH / "hogares.csv", funciones_hogares, nombres_hogares)

if __name__ == "__main__":
    unir_ambos_archivos()
    reemplazar_ambos_archivos()
    obtener_rango_fechas(dataset_path)