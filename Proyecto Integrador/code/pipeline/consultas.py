
from pipeline.rutas import PROCESADOS_PATH
import csv

aglomerados_eph = {
    "Gran La Plata": "2", "Bahía Blanca-Cerri": "3", "Gran Rosario": "4",
    "Gran Santa Fe": "5", "Gran Paraná": "6", "Posadas":  "7",
    "Gran Resistencia": "8", "Comodoro Rivadavia-Rada Tilly": "9", "Gran Mendoza": "10",
    "Corrientes": "12", "Gran Córdoba": "13", "Concordia": "14",
    "Formosa": "15", "Neuquén-Plottier": "17", "Santiago del Estero-La Banda": "18",
    "Jujuy-Palpalá": "19", "Río Gallegos": "20", "Gran Catamarca": "22",
    "Gran Salta": "23", "La Rioja": "25", "Gran San Luis": "26",
    "Gran San Juan": "27", "Gran Tucumán-Tafí Viejo": "29", "Santa Rosa-Toay": "30",
    "Ushuaia-Río Grande": "31", "Ciudad Autónoma de Buenos Aires": "32", "Partidos del Gran Buenos Aires": "33",
    "Mar del Plata": "34", "Río Cuarto": "36", "San Nicolás-Villa Constitución": "38",
    "Rawson-Trelew": "91", "Viedma-Carmen de Patagones": "93"
}
#----------------EJERCICIO 1---------------------------   
def porcentaje_alfabetizacion():
    """ Informa los porcentajes de la gente que es capaz/incapaz de leer
        por años, y ultimo trismestre"""
    
    try:
        with open (PROCESADOS_PATH/"individuos.csv") as archivo:
            
            lectura = csv.DictReader(archivo, delimiter= ";")
            
            info = {}
            info["0"] = {}
            for row in lectura:
                anio = row["ANO4"]
                tris = row["TRIMESTRE"]
                edad = row["CH06"]
                pondera = int (row["PONDERA"])
                sabe_leer = row["CH09"]

                if (anio not in info):
                        info[anio] = {
                        }

                if(tris not in info[anio]):
                    info[anio][tris] = {
                            "sabe leer" : 0,
                            "no sabe leer" : 0,
                            "total": 0
                    }

                if(edad > "6"):
                    match sabe_leer:
                        case "1":
                            info[anio][tris]["total"] += pondera
                            info[anio][tris]["sabe leer"] += pondera

                        case "2":
                            info[anio][tris]["total"] += pondera
                            info[anio][tris]["no sabe leer"] += pondera
    except FileNotFoundError :
        print("Se ve que el archivo de individuos no esta cargado")
    else:
        anio_max = max(info)   

        if(anio_max != "0"):
            tris_max = max(info[anio_max])
            aux = info[anio_max][tris_max]
            if(aux["total"] > 0):
                saben_leer = round(aux["sabe leer"] / aux["total"] * 100,2)
                no_saben = round(aux["no sabe leer"] / aux["total"] * 100,2)
                print(f"Datos del año : {anio_max} trismestre: {tris_max}")
                print(f"Unicamente saben leer y escribir el {saben_leer}%")
                print(f"No saben leer y escribir el {no_saben}%")

#----------------EJERCICIO 2---------------------------   
def Informar_universitarios_extranjeros():   
    """Informa los individuos no nacidos en Argentina con grado Universitario o superior"""
    with open(PROCESADOS_PATH/"individuos.csv") as archivo:
        lector = csv.DictReader(archivo, delimiter= ";")

        an04 = input("Elige un año (por ejemplo 2021): ")
        trim = input("Elige un trimestre (por ejemplo 1, 2, 3 o 4): ")
        
        extranjeros = 0
        universitarios = 0

        for row in lector:
            if row["ANO4"] == an04 and row["TRIMESTRE"] == trim:
                if row["CH15"] == "4" or "5":  # valores de = No nacido en Argentina
                    extranjeros += 1
                    if row["NIVEL_ED_str"] == "Superior o universitario":  # 6 = Universitario o superior
                        universitarios += 1
        
        if extranjeros > 0:
            porcentaje = (universitarios / extranjeros) * 100
            print(f"El {porcentaje:.2f}% de los no nacidos en Argentina tienen educación universitaria o superior.")
        else:
            print("No se encontraron personas no nacidas en Argentina para ese año y trimestre.")


#----------------EJERCICIO 3---------------------------        
def informar_desocupacion():
    """ Informa el año y trimestre con menor desocupacion que hubo"""
    try:
        with open(PROCESADOS_PATH/"individuos.csv") as archivo:
            lector = csv.DictReader(archivo, delimiter= ';')
        #Diccionario para guardar por cada años los trimestres
            info = {}
            

            for row in lector:
                anio = row["ANO4"]
                tris = row ["TRIMESTRE"]
                condicion = row["CONDICION_LABORAL"]
                pondera = int(row["PONDERA"])

                #Si no existe ese año en el diccionario lo agrego
                if(anio not in info):
                    info[anio] = {}
                    #si trismestre no esta en ese año lo agrego
                if(tris not in info[anio]):
                        #inicializo la cantidad de desocupados en 0
                        info[anio][tris] ={
                            "desocupados" : 0
                        }
                if(condicion == "Desocupado"):
                    info[anio][tris]["desocupados"] += pondera
    except FileNotFoundError:
        print("No hay archivos de individuos")
    else:
        #variables para calcular minimo
        anio_min = ""
        tris_min = ""
        minimo = 99999999
        for anio in sorted(info.keys(), reverse= True):
            for trismestre in sorted(info[anio].keys()):
                if(info[anio][trismestre]["desocupados"] < minimo):
                    minimo = info[anio][trismestre]["desocupados"]
                    anio_min = anio
                    tris_min = trismestre
        
        print(f'En el año {anio_min}, trismestre: {tris_min}')
        print(f'Fue en el que menos desocupados hubo: {minimo}')

#----------------EJERCICIO 4---------------------------   
def informar_rankings():
  
    fechas = {}
    with open(PROCESADOS_PATH / "individuos.csv") as archivo_individuos:
        lector = csv.DictReader(archivo_individuos, delimiter=";")
        for row in lector:
            anio = int(row["ANO4"])
            trimestre = int(row["TRIMESTRE"])
            if anio not in fechas:
                fechas[anio] = set()
            fechas[anio].add(trimestre)

    ultimo_anio = max(fechas)
    ultimo_trimestre = max(fechas[ultimo_anio])

    
    hogares_con_universitarios = set()
    codusu_aglomerado = {}

    with open(PROCESADOS_PATH / "individuos.csv") as archivo_individuos:
        lector = csv.DictReader(archivo_individuos, delimiter=";")
        for row in lector:
            if int(row["ANO4"]) == ultimo_anio and int(row["TRIMESTRE"]) == ultimo_trimestre:
                codusu = row["CODUSU"]
                aglo = int(row["AGLOMERADO"])
                codusu_aglomerado[codusu] = aglo
                if row["NIVEL_ED"] == "6":
                    hogares_con_universitarios.add(codusu)

    
    totales_por_aglo = {}  # aglo -> total hogares
    con_univ_por_aglo = {}  # aglo -> hogares con universitarios

    with open(PROCESADOS_PATH / "hogares.csv") as archivo_hogares:
        lector = csv.DictReader(archivo_hogares, delimiter=";")
        for row in lector:
            codusu = row["CODUSU"]
            if codusu in codusu_aglomerado:
                aglo = codusu_aglomerado[codusu]
                if int(row["IX_TOT"]) >= 2:
                    pondera = int(row["PONDERA"])
                    
                    if aglo not in totales_por_aglo:
                        totales_por_aglo[aglo] = 0
                    if aglo not in con_univ_por_aglo:
                        con_univ_por_aglo[aglo] = 0
                    
                    totales_por_aglo[aglo] += pondera

                    if codusu in hogares_con_universitarios:
                        con_univ_por_aglo[aglo] += pondera

    
    ranking = []
    for aglo in totales_por_aglo:
        total = totales_por_aglo[aglo]
        con_univ = con_univ_por_aglo.get(aglo, 0)
        porcentaje = (con_univ / total) * 100 if total > 0 else 0
        ranking.append((aglo, porcentaje))

    ranking.sort(key=lambda x: x[1], reverse=True)

    print(" Ranking de aglomerados con mayor % de hogares (2+ ocupantes) con universitarios:")
    for aglo, porcentaje in ranking[:5]:
        print(f"Aglomerado {aglo}: {porcentaje:.2f}%")
    print(f"Datos correspondientes al año {ultimo_anio}, trimestre {ultimo_trimestre}")

#----------------EJERCICIO 5---------------------------   
def informar_porcentaje_viviendas_ocupadas():
    """Informa el porcentajes de viviendas de cada aglomerado
        ocupado por sus propietarios"""
    try:
        with open(PROCESADOS_PATH/"hogares.csv") as archivo:
            
            lector = csv.DictReader(archivo, delimiter=";")
            #creo un diccionario para guardar por aglomerado total y propiedad propia
            info_aglo = {}
            for row in lector:
                aglomerado = row["AGLOMERADO"]
                hogar = row["II7"]
                pondera = int(row["PONDERA"])

                if(aglomerado not in info_aglo):
                    info_aglo[aglomerado] = {
                        "total" : 0,
                        "propiedad propia": 0
                        }
                if(hogar in ["1","2"]):
                    info_aglo[aglomerado]["propiedad propia"] += pondera
                info_aglo[aglomerado]["total"] += pondera
    except FileNotFoundError:
        print("No se encontro el archivo")
    else:
    #ordeno el diccionario x orden numerico de aglomerado
        for clave,dato in sorted(info_aglo.items(), key= lambda x: int(x[0])):
            porcentaje = round(dato["propiedad propia"] / dato["total"] * 100,2 )
            print(f'La cantidad de viviendas ocupadas en :{clave}  es de {porcentaje} %')


#----------------EJERCICIO 6---------------------------   

def informar_viviendas_sin_baños():
    """Informa el aglomerado con mayor cantidadad de viviendas con 2 o mas
    personas y sin ban0 """

    with open(PROCESADOS_PATH/"hogares.csv") as archivo_hogares:
        lector = csv.DictReader(archivo_hogares,delimiter=";")
        aglomerados = {}
        for row in lector:
            if(row["AGLOMERADO"] not in aglomerados):   #Cargo el diccionario de aglomerados
                aglomerados[row["AGLOMERADO"]] =  {
                    "cantidad_viviendas" : 0
                            }
            if (row["IX_TOT"] > "2") and (row["IV8"] == "2"): #Consulto si no tiene bano y si tiene 2 ocupantes
                aglomerados[row["AGLOMERADO"]]["cantidad_viviendas"] += (1 * int(row["PONDERA"]))

    aglomerado_max = max(aglomerados, key=lambda x:aglomerados[x]["cantidad_viviendas"])

    print(f"El aglomerado mas grande es el:{aglomerado_max}")
    print(f"La cantidad de viviendas son:{aglomerados[aglomerado_max]["cantidad_viviendas"]}")            
                    


#----------------EJERCICIO 7---------------------------   

def informar_porcentaje_aglomerado_universitario():
    """ Informa el porcentaje por aglomerado de la cantidad de personas
    que cursaron al menos en la universidad"""
    try:
        with open(PROCESADOS_PATH/"individuos.csv") as archivo_individuos:

            lector = csv.DictReader(archivo_individuos, delimiter= ";")
            info = {}
            for row in lector:
                aglomerado = row["AGLOMERADO"]
                educacion = row["NIVEL_ED_str"]
                pondera = int(row["PONDERA"])

                if(aglomerado not in info):
                    info[aglomerado] ={
                        "total":0,
                        "universitarios":0
                    }
                if(educacion in "Superior o universitario"):
                    info[aglomerado]["universitarios"] += pondera
                info[aglomerado]["total"] += pondera
    except FileNotFoundError:
        print("No se encuentra archivos de individuos")
    else:
        for clave,dato in sorted(info.items(), key= lambda x: int(x[0])):
            porcentaje = round(dato["universitarios"] / dato["total"] * 100,2 )
            print(f"En el aglomerado :{clave}")
            print(f'Cursaron la universidad o superior almenos un {porcentaje} %')
            
#----------------EJERCICIO 8---------------------------   
            
def informar_regiones():
    """Informa las regiones en orden decensdiente segun el porcentaje de inquiinos
    en cada una"""
    try:
        with open(PROCESADOS_PATH/"hogares.csv") as archivo_hogares:
            
            lector = csv.DictReader(archivo_hogares, delimiter=";")
            regiones = {}
            for row in lector:
                if (row["REGION"] not in regiones):
                    regiones[row["REGION"]] = {
                        "inquilinos" : 0,
                        "total" : 0
                    }
                if(row["II7"] == "3"):
                    regiones[row["REGION"]]["inquilinos"] += int(row["PONDERA"])
                regiones[row["REGION"]]["total"] += int(row["PONDERA"])
    except FileNotFoundError:
        print("No existe el archivo")
    else:
        regiones_ordenadas = sorted(
        regiones.items(),
        key=lambda x: (x[1]["inquilinos"] / x[1]["total"]) if x[1]["total"] > 0 else 0,
        reverse=True
        )

        for region, datos in regiones_ordenadas:
            porcentaje = (datos["inquilinos"] / datos["total"]) * 100
            print(f"Region {region}: {porcentaje: .2f} % de inquilinos \
                ({datos['inquilinos']} de {datos['total']})")
            
#----------------EJERCICIO 9---------------------------   


def tabla_de_aglomerados_mayores_edad(tabla = {}):
    """Retorna una tabla ordenada por año y trimestre de un aglomerado en donde se informa
        el nivel maximo de estudio que hizo una persona"""

    aglomerado = input("elija un aglomerados de los ya mostrados")
    if(aglomerado in aglomerados_eph):
        #si esta el aglomerados entonces busco en el archivo los datos
        aglomerado_index = aglomerados_eph[aglomerado]

        try:
            with open(PROCESADOS_PATH/"individuos.csv") as archivo:
            
                lector = csv.DictReader(archivo,delimiter= ";")
                
                for row in lector:
                    anio = row["ANO4"]
                    tris = row["TRIMESTRE"]
                    aglo = row["AGLOMERADO"]
                    educacion = row["NIVEL_ED_str"]
                    edad = row["CH06"]
                    pondera = int(row["PONDERA"])

                    if(anio not in tabla):
                        tabla[anio] = {}
                    if(tris not in tabla[anio]):
                        tabla[anio] [tris] = {
                        "Primario incompleto": 0,
                            "Primario completo": 0,
                            "Secundario incompleto": 0,
                            "Secundario completo": 0,
                            "Superior o universitario": 0
                        }
                        #Si el aglomerado es el mismo que el elegido y si es mayor de edad elegida 
                    if(aglo == aglomerado_index) and (edad >= "18"):
                        match educacion:
                            case "Primario incompleto":
                                tabla[anio][tris]["Primario incompleto"] += pondera
                            case "Primario completo" : 
                                tabla[anio][tris]["Primario completo"] += pondera
                            case "Secundario incompleto":
                                tabla[anio][tris]["Secundario incompleto"] += pondera
                            case "Secundario completo" : 
                                tabla[anio][tris]["Secundario completo"] += pondera
                            case "Superior o universitario":
                                tabla[anio][tris]["Superior o universitario"] += pondera
        except FileNotFoundError:
            print("Archivo no encontrado")
        else:
            #Creo una funcion para imprimir  
            def imprimir_tabla(tabla):  
                print(f'Aglomerado: {aglomerado} ')
                print("-"*135)
                print(f"{'Año':<5} {'Trimestre':<20} {'Primario':<20} {"Primario":<20} {"Secundario":<20} {'Secundario':<20} {'Superior o universitario'}")
                print(f"{'':<25} {'incompleto':<21} {'completo':<20} {'incompleto':<21} {'completo':<20}")
                print("-"*135)

                for anios in dict(sorted(tabla.items(), key= lambda x:x[0])):
                    for trismestre in dict(sorted(tabla[anios].items(), key= lambda x:x[0])):
                        datos = tabla[anios][trismestre]
                        print(f'{anios :<10} {trismestre :<17} {datos["Primario incompleto"]:<20} {datos["Primario completo"]} \
                    {datos["Secundario incompleto"]:< 20} {datos["Secundario completo"]:<5} \
                            {datos["Superior o universitario"]}')
                print("-"*135)

            return imprimir_tabla(tabla)
    else:
        print("-"*40)
        return print(f"Localidad inexistente o mal escrita")    
#----------------EJERCICIO 10---------------------------   

def mayores_de_edad_sin_secundario():

    aglo_1 = input("Ingrese un aglomerado para hacer la tabla")
    aglo_2 = input("Ingrese un segundo aglomerado")


    if(aglo_1 in aglomerados_eph) and (aglo_2 in aglomerados_eph):
        aglo1_index = aglomerados_eph[aglo_1]
        aglo2_index = aglomerados_eph[aglo_2]
        informacion = {}
        try:
            with open (PROCESADOS_PATH/"individuos.csv") as archi_indi:

                lector = csv.DictReader(archi_indi,delimiter=";")

                for row in lector:
                    anio = row["ANO4"]
                    tris = row["TRIMESTRE"]
                    edad = row["CH06"]
                    educacion = row["NIVEL_ED_str"]
                    aglo = row["AGLOMERADO"]
                    pondera = int(row["PONDERA"])
                    if(anio not in informacion):
                        informacion[anio] = {}
                    
                    if(tris not in informacion[anio]):
                        informacion[anio][tris] = {
                            aglo_1 :{
                                "total":0,
                                "Secundario incompleto": 0,
                                "porcentaje" : 0
                            },
                            aglo_2 : {
                                "total":0,
                                "Secundario incompleto": 0,
                                "porcentaje" : 0
                            }
                        }

                    if (aglo == aglo1_index):
                        informacion[anio][tris][aglo_1]["total"] += pondera
                        if(edad > "18") and (educacion == "Secundario incompleto"):
                            informacion[anio][tris][aglo_1]["Secundario incompleto"] += pondera
                    if(aglo == aglo2_index):
                        informacion[anio][tris][aglo_2]["total"] += pondera
                        if(edad > "18") and (educacion == "Secundario incompleto"):
                            informacion[anio][tris][aglo_2]["Secundario incompleto"] += pondera
        except FileNotFoundError:
            print("Archivo no encontrado")
        else:
            for anio in sorted(informacion.keys()):
                for tris in sorted(informacion[anio].keys()):
                    aux = informacion[anio][tris][aglo_1]
                    aux["porcentaje"] = round(aux["Secundario incompleto"] / aux["total"] * 100,2)
                    aux = informacion[anio][tris][aglo_2]
                    aux["porcentaje"] = round(aux["Secundario incompleto"] / aux["total"] * 100,2)

            def imprimir_tabla(tabla):
                print("-"*70)
                print(f"{'Año':<5} {'Trimestre':<20} {aglo_1:<20} {aglo_2:<20}")
                print("-"*70)
                for anio in sorted(tabla.keys()):
                    for tris in sorted(tabla[anio].keys()):
                        aux = tabla[anio][tris]
                        print(f"{anio:<10} {tris:<15} {aux[aglo_1]["porcentaje"]}{"%":<20} {aux[aglo_2]["porcentaje"]}{"%":<20}")
                        
            return imprimir_tabla(informacion)
    else:
        print("Algunos de los aglomerados no existe")

#----------------EJERCICIO 11---------------------------   

def aglomerados_precarios():
    """Informa el porcentaje del aglomerado con mayor y mennor porcentaje
    de viviendas de material precario"""

    anio_read = input("Ingrese un año para buscar")
    info ={}
    try:
        with open(PROCESADOS_PATH/"hogares.csv") as archi_hogares:
            lector = csv.DictReader(archi_hogares, delimiter= ";")

            for row in lector:
                if(row["ANO4"] == anio_read):    
                    anio = row["ANO4"]
                    tris = row["TRIMESTRE"]
                    aglomerado = row["AGLOMERADO"]
                    pondera = row["PONDERA"]
                    material = row["MATERIAL_TECHUMBRE"]

                    if(anio not in info):
                        info[anio]={}

                    if(tris not in info[anio]):
                        info[anio][tris] = {}

                    if(aglomerado not in info[anio][tris]):
                        info[anio][tris][aglomerado] = {
                            "precario":0,
                            "total":0,
                            "porcentaje":0
                        }

                    if(material == "Material precario"):
                        info[anio][tris][aglomerado]["precario"]+= int(pondera)
                    info[anio][tris][aglomerado]["total"]+= int(pondera)
    except FileNotFoundError:
        print("Archivo no encontrado")
    else:
        ultimo_trismestre = max (info[anio_read])

        for dato in info[anio_read][ultimo_trismestre].values():
            if(dato["total"] > 0): 
                porcentaje = round(dato["precario"] / dato["total"] * 100,3)
                dato["porcentaje"] = porcentaje
     
        aglo_max = ""
        aglo_min = ""
        maximo =  -1
        minimo = 101

        for aglomerado, dato in info[anio_read][ultimo_trismestre].items():
            if(dato["porcentaje"] > maximo):
                maximo = dato["porcentaje"]
                aglo_max = aglomerado
            if(dato["porcentaje"] < minimo):
                minimo = dato["porcentaje"]
                aglo_min = aglomerado
            
        print(f" el aglomerado con mayor porcentaje fue : {aglo_max} con {float(maximo)}%")
        print(f" el aglomerado con menor porcentaje fue : {aglo_min} con {float(minimo)}%")

#----------------EJERCICIO 12---------------------------   

def jubilados_situacion_hogar_complicada():
    """Informe para cada aglomerado de los jubilados con condicion de habitabilidad insuficiente """
    fechas = {}
    with open(PROCESADOS_PATH / "individuos.csv") as archivo_individuos:
        lector = csv.DictReader(archivo_individuos, delimiter=";")
        for row in lector:
            anio = int(row["ANO4"])
            trimestre = int(row["TRIMESTRE"])

            if anio not in fechas:
                fechas[anio] = set()
            fechas[anio].add(trimestre)

    # Encontramos el último año y trimestre
    ultimo_anio = max(fechas)
    ultimo_trimestre = max(fechas[ultimo_anio])

    # Diccionario para contar jubilados por aglomerado
    jubilados = {}
    codusu_aglomerado = {}  # Para luego cruzar con hogares

    with open(PROCESADOS_PATH / "individuos.csv") as archivo_individuos:
        lector = csv.DictReader(archivo_individuos, delimiter=";")
        for row in lector:
            anio = int(row["ANO4"])
            trimestre = int(row["TRIMESTRE"])

            if anio == ultimo_anio and trimestre == ultimo_trimestre:
                if row["CAT_INAC"] == "1":  # Jubilado
                    aglo = int(row["AGLOMERADO"])
                    codusu = row["CODUSU"]

                    if aglo not in jubilados:
                        jubilados[aglo] = {"total": 0, "insuficiente": 0}
                    jubilados[aglo]["total"] += int(row["PONDERA"])  # usar ponderador
                    codusu_aglomerado[codusu] = aglo

    with open(PROCESADOS_PATH/"hogares.csv") as archivo_hogares:
        lector = csv.DictReader(archivo_hogares,delimiter=";")
        for row in lector:
            codusu = row["CODUSU"]
            if codusu in codusu_aglomerado:
                aglo = codusu_aglomerado[codusu]
                if row["CONDICION_DE_HABITABILIDAD"] == "Insuficiente":
                    jubilados[aglo]['insuficiente'] += int(row["PONDERA"])
    
    def imprimir_jubilados():
        for aglo, datos in sorted(jubilados.items()):
            total = datos["total"]
            insuficiente = datos["insuficiente"]
            porcentaje = (insuficiente/total) * 100 if total > 0 else 0
            print(f"Aglomerado {aglo}: {porcentaje:.2f}% jubilados en viviendas\
 con habitabilidad insuficiente")                
    return imprimir_jubilados() 

#----------------EJERCICIO 13---------------------------   
def universitarios_en_condiciones_insuficientes():
    """Informa a partir de un año en el ultimo trismestre disponible
    la cantidad de personas que cursaron en nivel universitario o superior
    y que viven en una condicion insuficiente"""

    #Limites de años para buscar
    anio_min = "2020"
    anio_max = "2024"
    anio_buscado = input(f"Ingrese un año entre {anio_min} y {anio_max}")
    
    #verifico que el año ingresado cumpla los limites
    if(anio_buscado > anio_min or anio_buscado <= anio_max): 
        universitarios = 0
        try:
            with open(PROCESADOS_PATH/"individuos.csv") as archivo_indi:        
                
                lector = csv.DictReader(archivo_indi, delimiter= ";")

                informacion = {
                    "0": 0
                }
                for row in lector:

                    codusu = row["CODUSU"]
                    anio = row["ANO4"]
                    educacion = row["NIVEL_ED_str"]
                    tris = row["TRIMESTRE"]

                    if(anio == anio_buscado) and (educacion == "Superior o universitario"):
                        if(tris not in informacion):
                            informacion[tris] = {
                                "lista": []
                            }
                        informacion[tris]["lista"].append(codusu)
        except FileNotFoundError:
            print("Archivo no encontrado")
        else:

            ultimo_tris = max(informacion)
            #si dicho año tiene trismestres analizo en el otro archivo
            if(ultimo_tris > "0"):
                lista_codusu = informacion[ultimo_tris]["lista"]
                with open(PROCESADOS_PATH/"hogares.csv")as archi_hog:
                    
                    lector = csv.DictReader(archi_hog,delimiter=";")

                    for row in lector:
                        anio = row["ANO4"]
                        codusu = row["CODUSU"]
                        tris = row["TRIMESTRE"]
                        condicion =row["CONDICION_DE_HABITABILIDAD"]
                        pondera = int(row["PONDERA"])

                        if(anio == anio_buscado) and (tris == ultimo_tris):
                            if(codusu in lista_codusu) and (condicion == "Insuficiente"):
                                universitarios+= pondera

                #imprimo la informacion
                print("-"*50)
                print(f"Año: {anio_buscado}  Trimestre: {ultimo_tris}")
                print(f"Posee un total de {universitarios} de personas que cursan o cursaron viviendo en condiciones insuficientes")
            else:
                #En caso que no haya trimestre en el año ingresado
                print("Dicho año no tiene trimestres cargados en el sistema")
    else:
        #En caso de ingresar un año inferior o superior al limite
        print("El año ingresado no se puede buscar")

            
