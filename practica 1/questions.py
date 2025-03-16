import random
# Preguntas para el juego
questions = [
    "¿Qué función se usa para obtener la longitud de una cadena en Python?",
    "¿Cuál de las siguientes opciones es un número entero en Python?",
    "¿Cómo se solicita entrada del usuario en Python?",
    "¿Cuál de las siguientes expresiones es un comentario válido en Python?",
    "¿Cuál es el operador de comparación para verificar si dos valores son iguales?",
]
# Respuestas posibles para cada pregunta, en el mismo orden que las preguntas
answers = [
    ("size()", "len()", "length()", "count()"),
    ("3.14", "'42'", "10", "True"),
    ("input()", "scan()", "read()", "ask()"),
    (
        "// Esto es un comentario",
        "/* Esto es un comentario */",
        "-- Esto es un comentario",
        "# Esto es un comentario",
    ),
    ("=", "==", "!=", "==="),
]
# Índice de la respuesta correcta para cada pregunta, el el mismo orden que las preguntas
correct_answers_index = [1,2,0,3,1]
#2, 3, 1, 4, 2 correctas

questions_to_ask = random.choices(list(zip(questions,answers,correct_answers_index)), k=3)

# El usuario deberá contestar 3 preguntas
puntos = 0.0
for preg,res,correct in questions_to_ask:
    # Se selecciona una pregunta aleatoria
    # Recorro la lista de respuestas e imprimo
    print (preg)
    for i, r in enumerate(res):
        print (f'{i + 1}: {r}')


    # El usuario tiene 2 intentos para responder correctamente
    for intento in range(2):
        user_answer = input("Respuesta: ")

    # Checkeo si ingreso num fuera de rango o cadena, si da true exiteo con 1
        if not user_answer.isnumeric() or int(user_answer)-1 not in range(len(res)):
            print("Respuesta no valida")
            exit(1)

    # Se verifica si la respuesta es correcta y sumo puntos   
        if int(user_answer) - 1 == correct:
            puntos += 1
            print("¡Correcto!")
            break
        else:
        # Si el usuario no responde correctamente después de 2 intentos, se muestra la respuesta correcta
        # Resto puntos
         puntos -= 0.5
         if intento == 1:
            print("Incorrecto. La respuesta correcta es: " + str(res[correct]))
            
print("Puntos Totales: " + str(puntos))