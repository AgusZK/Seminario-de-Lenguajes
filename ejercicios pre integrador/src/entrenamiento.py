import csv

path_individuos = 'ejercicios pre integrador/files/usu_individual_T324.txt'
path_hogares = 'ejercicios pre integrador/files/usu_hogar_T324.txt'

# ---------------- INDIVIDUOS --------------------
cantM = 0
cantF= 0
mayoresYestudios = 0
with open(path_individuos) as csv_individuos:
   reader = csv.reader(csv_individuos,delimiter= ';')
   header = next(reader)

   # INDICE DE CADA COLUMNA EN INDIVIDUOS
   SEXO_INDEX = 11
   PONDERA = 9
   EDAD_INDEX = 13
   ESTUDIOS_INDEX = 26

   for r in reader:
      # SI ES HOMBRE LO SUMO, SINO ES MUJER
      if r[SEXO_INDEX] == '1':
         cantM= cantM + int(r[PONDERA])
      else:
         cantF= cantF + int(r[PONDERA])
      # SI ES MAYOR DE EDAD Y TIENE EL SECUNDARIO COMPLETO LO SUMO
      if r[EDAD_INDEX] >= '18' and r[ESTUDIOS_INDEX] == '4': 
         mayoresYestudios = mayoresYestudios + int(r[PONDERA])

print(f'Hombres: {cantM} || Mujeres: {cantF}')
print(f'Personas adultas con secundario terminado: {mayoresYestudios}')

# ---------------- HOGARES --------------------  
viviendasTotales = 0
viviendasProp = 0
with open(path_hogares) as csv_hogares:
   # CREO READER Y HEADER PARA RECORRER
   readerH = csv.reader(csv_hogares, delimiter=';')
   headerH = next(readerH)
   # INDICES DE CADA COLUMNA EN HOGARES
   PONDERA_H = 8
   TENENCIA_INDEX = 37
   BANIO_INDEX = 19
   HABITANTES_INDEX= 64
   AGLOMERADO_INDEX = 7
   # ME CREO UN DICCIONARIO PARA IR SUMANDO CANTIDAD Y OTRO CON LOS NOMBRES
   aglomerados = {}
   aglomeradosNombres = {'02':'Gran La Plata', '03':'Bahia Blanca - Cerri', '04':'Gran Rosario',
                         '05':'Gran Santa Fe', '06':'Gran Parana','07':'Posadas','08':'Gran resistencia',
                         '09':'Comodoro Rivadavia - Rada tilly', '10':'Gran Mendoza', '12':'Corrientes',
                         '13':'Gran Cordoba', '14':'Concordia' , '15':'Formosa', '17':'Neuquen - Plottier',
                         '18':'Santiago del Estero - La Banda', '19':'Jujuy - Palpala', '20':'Rio Gallegos',
                         '22':'Gran Catamaca', '23':'Gran Salta', '25':'La Rioja', '26':'Gran San Luis', '27':'Gran San Juan',
                         '29':'Gran Tucuman - Tafi Viejo', '30':'Santa Rosa - Toay', '31':'Ushuaia - Rio grande', '32':'Ciudad Autonoma de Buenos Aires',
                         '33':'Partidos del GBA', '34':'Mar del Plata', '36':'Rio Cuarto', '38':'San Nicolas - Villa Constitucion',
                         '91':'Rawson - Trelew', '93':'Viedma - Carmen de Patagones'}
   
   for rh in readerH:
      # SUMO TODAS LAS VIVIENDAS Y LAS QUE CUMPLEN CONDICION POR SEPARADO
      viviendasTotales = viviendasTotales + int(rh[PONDERA_H])
      if rh[TENENCIA_INDEX] == '1':
         viviendasProp = viviendasProp + int(rh[PONDERA_H])
      
      # ME FIJO QUE TENGA BANIO Y QUE VIVAN MAS DE 2, SI CUMPLE CONDICION LO SUMO AL DICCIONARIO SI EXISTE Y SINO LO CREO
      if rh[BANIO_INDEX] == '1' and rh[HABITANTES_INDEX] > '2':
         clave = rh[AGLOMERADO_INDEX]
         if clave in aglomerados:
            aglomerados[clave] += int(rh[PONDERA_H])
         else:
            aglomerados[clave] = int(rh[PONDERA_H])

# IMPRIMO EL PORCENTAJE DE VIVIENDAS OCUPADAS POR PROPIETARIOS POR SOBRE EL TOTAL DE VIVIENDAS
print(f'El porcentaje de viviendas ocupadas por el propietario de vivienda y terreno es: {((viviendasProp/viviendasTotales) * 100):.1f} %')
# LE PASO A MAX EL DICCIONARIO Y ME DEVUELVE LA KEY CON MAYOR CANTIDAD, LA CUAL LA USO COMO INDICE EN AGLOMERADOSNOMBRES
maxAglomerado = max(aglomerados,key=aglomerados.get)
print(f'El aglomerado con mayor cantidad de viviendas con mas de 2 ocupantes es: {aglomeradosNombres[maxAglomerado]}')