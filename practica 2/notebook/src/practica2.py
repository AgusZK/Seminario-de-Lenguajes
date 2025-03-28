import string
import random
# PUNTO 1
zen_text = ["Beautiful is better than ugly.",
            "Explicit is better than implicit.",
            "Simple is better than complex.",
            "Complex is better than complicated.",
            "Flat is better than nested.",
            "Sparse is better than dense.",
            "Readability counts.",
            "Special cases aren't special enough to break the rules.",
            "Although practicality beats purity.",
            "Errors should never pass silently.",
            "Unless explicitly silenced.",
            "In the face of ambiguity, refuse the temptation to guess.",
            "There should be one-- and preferably only one --obvious way to do it.",
            "Although that way may not be obvious at first unless you're Dutch.",
            "Now is better than never.",
            "Although never is often better than *right* now.",
            "If the implementation is hard to explain, it's a bad idea.",
            "If the implementation is easy to explain, it may be a good idea.",
            "Namespaces are one honking great idea -- let's do more of those!"]

vocals = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]

#for elem in zen_text:
#    if elem[1] in vocals:
#        print(elem)

# PUNTO 2

titles = ["Speedrun de Super Mario en tiempo récord","Charla sobre desarrollo de videojuegos",
          "Jugando al nuevo FPS del momento con amigos",
          "Música en vivo: improvisaciones al piano"]

#maxAux = 0
#maxT = ""
#for title in titles:
    #if (maxAux < len(title)):
      #  maxT = title
        #maxAux = len(title)
#print(f'(El titulo mas largo es: {maxT}')

# PUNTO 3

rules = """Respeta a los demás. No se permiten insultos ni lenguaje
ofensivo.
Evita el spam. No publiques enlaces sospechosos o repetitivos.
No compartas información personal.
Usa los canales adecuados para cada tema.
Sigue las instrucciones de los moderadores."""

#keyword = input("Introduce una palabra clave: ")

#for rule in rules.split("\n"):
#    if keyword in rule:
#        print(rule)

# PUNTO 4

def validar(name):
    if len(name) < 5:
        return "El nombre no cumple con los requisitos"

    # Si no tiene numeros
    if not any(char.isdigit() for char in name):
        return "El nombre no cumple con los requisitos"

    ## Si algun char no es mayus
    if not any(char.isupper() for char in name):
        return "El nombre no cumple con los requisitos"
    
    # Si tiene algo q no sea num o letra
    if not name.isalnum():
        return "El nombre no cumple con los requisitos"
    
    return "Nombre de usuario valido"
    


# PUNTO 5

#time = int(input("Ingrese su tiempo de reacción en ms: "))

def clasificar(time):
    if (time < 200):
        return "Rapido"
    elif (200 <= time <= 500):
        return "Normal"     
    else:
        return "Lento"

# PUNTO 6
descriptions = [
"Streaming de música en vivo con covers y composiciones",
"Charla interactiva con la audiencia sobre series y películas",
"Jugamos a juegos retro y charlamos sobre su historia",
"Exploramos la mejor música de los 80s y 90s",
"Programa de entretenimiento con noticias y curiosidades del mundo gamer",
 "Sesión de charla con invitados especiales del mundo del streaming",
"Música en directo con improvisaciones y peticiones del chat",
"Un espacio para charlar relajada sobre tecnología y cultura digital",
"Exploramos el impacto de la música en los videojuegos clásicos"]

count = {"música": 0 , "charla": 0 , "entretenimiento": 0}
words = ["música", "charla", "entretenimiento"]

for desc in descriptions:
    for w in words:
        if w.lower() in desc.lower():
            count[w] += 1

#print("Menciones a musica: ", count["música"])
#print("Menciones a charla: ", count["charla"])
#print("Menciones a entretenimiento: ", count["entretenimiento"])


# PUNTO 7

#name = input('Ingrese nombre de usuario (max 15 char) ')
chars = string.ascii_uppercase + string.digits


def generar_codigo (name,chars):
    if len(name) > 15:
        return "El nombre de usuario es muy largo"
    else:
        s = name.upper() + '-' + "20242703" + "-"
        # .JOIN TRANSFORMA LA LISTA DEL RANDOM EN STRING PARA CONCATENAR
        code = ''.join(random.choices(chars, k = (30-len(s))))
        return(s + code)

#print (generar_codigo(name,chars))

# PUNTO 8

#word1 = input("Ingrese la primer palabra: ")
#word2 = input("Ingrese la segunda palabra: ")

def anagramas(word1,word2):
    if len(word1) > len(word2) or len(word2) > len (word1):
        return "No son anagramas."
    elif sorted(word1) == sorted(word2):
        return "Son anagramas"
    else:
        return "No son anagramas."

#print(anagramas(word1,word2))

# PUNTO 9

clients = [" Ana López ", "Pedro Gómez", "maria martínez", "Pedro Gómez ", "",
" Luis Rodríguez ", None, "ana lópez", "JUAN PÉREZ", "MARTA SUÁREZ",
"luis rodríguez", "maría martínez ", " claudia torres", "CLAUDIA TORRES",
" ", "pedro gómez", "Juan Pérez", None, "Ricardo Fernández", "LAURA RAMOS",
"carlos mendes", "RICARDO FERNÁNDEZ ", " Laura ramos", "CARLOS MENDES",
"alejandro gonzález", " ALEJANDRO GONZÁLEZ ", "Patricia Vega",
"patricia VEGA", "Andrés Ocampo", " andrés ocampo", "Monica Herrera",
"MONICA HERRERA ", "gabriela ruíz", "Gabriela Ruíz", "sandra morales",
"SANDRA MORALES", "miguel ángel", "Miguel Ángel ", " Damián Castillo",
"Damián Castillo ", None, "", " "]

def clean_clients(clients):
    clean_list = []
    for cli in clients:
        if cli:
            # ME FIJO Q NO SEA NONE
            if cli not in clean_list:
            # SI NO ESTA, SACO ESPACIOS, AGREGO MAYUS Y LO AGREGO A UNA LISTA NUEVA
             clean_list.append(cli.strip().title())
    return clean_list

#print(clean_clients(clients))       


# PUNTO 10

# rounds = [
# {
# 'Shadow': {'kills': 2, 'assists': 1, 'deaths': True},
# 'Blaze': {'kills': 1, 'assists': 0, 'deaths': False},
# 'Viper': {'kills': 1, 'assists': 2, 'deaths': True},
# 'Frost': {'kills': 0, 'assists': 1, 'deaths': False},
# 'Reaper': {'kills': 1, 'assists': 1, 'deaths': False}
# },
# {
# 'Shadow': {'kills': 0, 'assists': 2, 'deaths': False},
# 'Blaze': {'kills': 2, 'assists': 0, 'deaths': True},
# 'Viper': {'kills': 1, 'assists': 1, 'deaths': False},
# 'Frost': {'kills': 2, 'assists': 1, 'deaths': True},
# 'Reaper': {'kills': 0, 'assists': 1, 'deaths': False}
# },
# {
# 'Shadow': {'kills': 1, 'assists': 0, 'deaths': False},
# 'Blaze': {'kills': 2, 'assists': 2, 'deaths': True},
# 'Viper': {'kills': 1, 'assists': 1, 'deaths': True},
# 'Frost': {'kills': 0, 'assists': 1, 'deaths': False},
# 'Reaper': {'kills': 1, 'assists': 1, 'deaths': False}
# },
# {
# 'Shadow': {'kills': 2, 'assists': 1, 'deaths': False},
# 'Blaze': {'kills': 1, 'assists': 0, 'deaths': True},
# 'Viper': {'kills': 0, 'assists': 2, 'deaths': False},
# 'Frost': {'kills': 1, 'assists': 1, 'deaths': True},
# 'Reaper': {'kills': 1, 'assists': 1, 'deaths': False}
# },
# {
# 'Shadow': {'kills': 1, 'assists': 2, 'deaths': True},
# 'Blaze': {'kills': 0, 'assists': 1, 'deaths': False},
# 'Viper': {'kills': 2, 'assists': 0, 'deaths': True},
# 'Frost': {'kills': 1, 'assists': 1, 'deaths': False},
# 'Reaper': {'kills': 1, 'assists': 1, 'deaths': True}
# }
# ]

# # INICIALIZO TABLA PARA CONTAR AL FINAL
# players = {
#     'Shadow': {'kills': 0, 'assists': 0, 'deaths': 0, 'mvp_count': 0, 'total_points': 0},
#     'Blaze': {'kills': 0, 'assists': 0, 'deaths': 0, 'mvp_count': 0, 'total_points': 0},
#     'Viper': {'kills': 0, 'assists': 0, 'deaths': 0, 'mvp_count': 0, 'total_points': 0},
#     'Frost': {'kills': 0, 'assists': 0, 'deaths': 0, 'mvp_count': 0, 'total_points': 0},
#     'Reaper': {'kills': 0, 'assists': 0, 'deaths': 0, 'mvp_count': 0, 'total_points': 0}
# }

# for round in rounds:
#     # CREO UN DICT PARA CONTAR LOS PUNTOS DE LA RONDA
#     points = {}
#     # USO TUPLA PARA RECORRER, KEY = 'PLAYER', VALUE = {DICT DE STATS}
#     for player, stats in round.items():
#         # GUARDO STATS Y CREO UN DICCIONARIO PLAYER:PUNTOS
#         kills = stats['kills']
#         assists = stats['assists']
#         deaths = 1 if stats['deaths'] else 0
#         total_points = kills * 3 + assists * 1 - deaths
#         points[player] = total_points

#         # ACTUALIZO EN TABLA GENERAL
#         players[player]['kills']+= kills
#         players[player]['assists']+= assists
#         players[player]['deaths']+= deaths
#         players[player]['total_points']+= total_points  

#     # LE PASO A MAX EL DICCIONARIO Y ME DEVUELVE LA KEY CON MAYOR PUNTOS, LA USO DE INDICE PARA SUMAR 1
#     mvp = max(points,key=points.get)
#     players[mvp]['mvp_count']+= 1

#     # ROUND.INDEX ME DICE LA POS DEL VALOR DE ROUND
#     print(f'\nRanking ronda {rounds.index(round) + 1}:')

      # IMPRIMO TABLA POR RONDA
#     print(f'\n{'Jugador':<5} {'Kills':>6} {'Asistencias':>17} {'Muertes':>11} {'Puntos':>11}')
#     print("--------------------------------------------------------")        
#     for player in round:
#         kills = round[player]['kills']
#         assists = round[player]['assists']
#         deaths = 1 if round[player]['deaths'] else 0
#         total_points = kills * 3 + assists * 1 - deaths
#         print(f'{player:<10} {kills:<7} {assists:>8} {deaths:>13} {total_points:>11}')

# print(f'\nRanking final:')
# print(f'\n{'Jugador':<5} {'Kills':>6} {'Asistencias':>17} {'Muertes':>11} {'MVPS':>10} {'Puntos':>11}')
# print("-------------------------------------------------------------------")        
# for player in players:
#     kills = players[player]['kills']
#     assists = players[player]['assists']
#     deaths = players[player]['deaths']
#     mvps = players[player]['mvp_count']
#     total_points = players[player]['total_points']
#     print(f'{player:<10} {kills:<7} {assists:>8} {deaths:>13} {mvps:>13} {total_points:>11}')