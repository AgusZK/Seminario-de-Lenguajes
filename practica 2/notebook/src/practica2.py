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

max = 0
maxT = ""
for title in titles:
    if (max < len(title)):
        maxT = title
        max = len(title)
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

print("Menciones a musica: ", count["música"])
print("Menciones a charla: ", count["charla"])
print("Menciones a entretenimiento: ", count["entretenimiento"])
