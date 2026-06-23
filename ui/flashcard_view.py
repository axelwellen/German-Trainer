from tkinter import *
# debemos guardar:
# palabras, indice_actual, mostrar_significado
# ej: indice_actual = 0; mostrar_significado = False
#
# Elementos de la tarjeta:
# Parte superior: 
#   Palabra (3/20) - Nivel: B2 - Tipo: Sustantivo - Tags (arbeit, beruf)
# Centro:
#   Führungsposition
#   si es sustantivo: die Führungsposition
#   Pl: Führungsposition
#   si es verbo: Perfekt, Präteritum, Auxiliar, separable, reflexivo, ...
# Parte de abajo:
#   Botón de mostrar significado. Al pulsarlo vemos significados, Notas, Ejemplos?
# Botones inferiores:
#   Anterior, mostrar/ocultar, siguiente, aleatoria, vovler
# En el MVP: se puede añadir a favoritas

estado = {
        "palabras":[],
        "indice_actual":0,
        "mostrar_significado":False, 
        "start_vocab_callback": None, 
        "parent_frame":None
        }

# función llamada desde app.py
def render_flashcard_view(palabras, parent_frame, start_vocab_callback):
    estado["parent_frame"] = parent_frame
    estado["palabras"] = palabras
    estado["indice_actual"] = 0
    estado["mostrar_significado"] = False
    estado["start_vocab_callback"] = start_vocab_callback
    show_current_card()

# actualiza la pantalla con la palabra actual
def show_current_card():
    # tenemos que limpiar parent frame primero
    parent_frame = estado["parent_frame"]
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    palabras = estado["palabras"]
    indice = estado["indice_actual"]
    palabra_actual = palabras[indice]
    # titulo
    Label(parent_frame, text="Flashcards").pack(anchor = "w", pady=10)
    # parte superior
    word_header_frame = Frame(parent_frame)
    word_header_frame.pack(anchor = "w", padx = 20, pady = 10)
    render_word_header(word_header_frame, palabra_actual)
    # body frame
    word_body_frame = Frame(parent_frame)
    word_body_frame.pack(anchor = "w", padx = 20, pady = 10)
    render_word_body(word_body_frame, palabra_actual)
    # parte abajo (meaning, examples)
    if estado["mostrar_significado"]:
        word_meaning_frame = Frame(parent_frame)
        word_meaning_frame.pack(anchor = "w", padx = 20, pady = 10)
        render_meaning_section(word_meaning_frame, palabra_actual)
        word_examples_frame = Frame(parent_frame)
        word_examples_frame.pack(anchor = "w", padx = 20, pady = 10)
        render_examples_section(word_examples_frame, palabra_actual)
        extra_frame = Frame(parent_frame)
        extra_frame.pack(anchor = "w", padx = 20, pady = 10)
        render_extra_section(extra_frame, palabra_actual)
    # botones inferiores
    buttons_frame = Frame(parent_frame)
    buttons_frame.pack(anchor = "center")
    

    if estado["indice_actual"] == 0:
        btn_prev = Button(buttons_frame, text = "< Anterior", state="disabled")
    else:
        btn_prev = Button(buttons_frame, text = "< Anterior", command = previous_card)
    
    if estado["indice_actual"]==len(estado["palabras"])-1:
        btn_next = Button(buttons_frame, text = "Volver", command = go_back_to_vocab)
    else:
        btn_next = Button(buttons_frame, text = "Siguiente >", command = next_card)
    
    btn_show_meaning = Button(buttons_frame, text = "Mostrar significado", command = toogle_meaning)
    btn_show_meaning.config(width = 15, height = 2)
    btn_next.config(width = 15, height = 2)
    btn_prev.config(width = 15, height = 2)
    
    btn_prev.pack(side="left", padx=2, pady=5)
    btn_show_meaning.pack(side = "left", padx=2, pady=5)
    btn_next.pack(side="left", padx=2, pady=5)

# aumenta índice y muestra siguiente, si llega al final: 
# Volver al inicio, o mostrar "fin de lista"
def next_card():
    estado["indice_actual"] += 1
    show_current_card()

# retrocede índice
def previous_card():
    estado["indice_actual"] -= 1
    show_current_card()

# Cambiar mostrar_significado
def toogle_meaning():
    estado["mostrar_significado"] = not estado["mostrar_significado"]
    show_current_card()

# Elige una palbra aleatoria de la lista.
# Para el MVP no lo vamos a hacer
def random_card():
    pass

# muestra la info de la palabra en la parte superior
def render_word_header(parent_frame, palabra):
    # palabras 3/20
    indice = estado["indice_actual"]+1
    total_palabras = len(estado["palabras"])
    Label(parent_frame, text = f"Palabra {indice}/{total_palabras}"). grid(row=0, column = 0, sticky="w")
    # Nivel B2
    Label(parent_frame, text = f"Nivel: {palabra['datos']['nivel']}"). grid(row=0, column = 1, sticky="w")
    # Tipo: noun
    Label(parent_frame, text = f"Tipo: {palabra['datos']['tipo']}"). grid(row=0, column = 2, sticky="w")
    # Tags: arbeit, beruf
    tags = ""
    for i,tag in enumerate(palabra["tags"]):
        tags += tag
        if len(palabra["tags"]) > i+1:
            tags += ", "
    Label(parent_frame, text = f"Tags: {tags}"). grid(row=0, column = 3, sticky="w")

def render_word_body(parent_frame, palabra):
    texto = palabra["datos"]["palabra"]
    tipo = palabra["datos"]["tipo"]
    if tipo == "noun":
        articulo = obtener_articulo(palabra["datos"]["genero"])
        color = obtener_color_genero(palabra["datos"]["genero"])
        plural = palabra["datos"]["plural"]

        palabra_frame = Frame(parent_frame)
        palabra_frame.pack(anchor="w")

        Label(palabra_frame, text = articulo, fg=color).pack(side="left")
        Label(palabra_frame, text=f"{texto}").pack(side="left")

        if plural:
            Label(parent_frame, text = f"Plural: {plural}").pack(anchor="w")
    else:
        Label(parent_frame, text=texto).pack(anchor="w")

def obtener_color_genero(genero):
    if genero == "m":
        return "blue"
    elif genero == "f":
        return "red"
    elif genero == "n":
        return "green"
    elif genero == "pl":
        return "yellow"
    return "black"

def obtener_articulo(genero):
    if genero == "m":
        return "der"
    elif genero == "f":
        return "die"
    elif genero == "n":
        return "das"
    elif genero == "pl":
        return "die"
    return ""

def render_meaning_section(parent_frame, palabra):
    significados = palabra["significados"]
    Label(parent_frame, text = "Significados:").pack(anchor="w")
    for significado in significados:
        Label(parent_frame, text = f"- {significado}").pack(anchor="w")
    nota = palabra['datos']['notas']
    if nota != '""':
        Label(parent_frame, text = f"Nota: {nota}").pack(anchor="w")

# Aquí ponemos los ejemplos
def render_examples_section(parent_frame, palabra):
    ejemplos = palabra["ejemplos"]
    Label(parent_frame, text = "Ejemplos:").pack(anchor="w")
    for ejemplo in ejemplos:
        Label(parent_frame, text = f"DE: {ejemplo['ejemplo_de']}").pack(anchor="w")
        Label(parent_frame, text = f"ES: {ejemplo['ejemplo_es']}\n").pack(anchor="w")
    
# Aquí pondremos los extras como los sinónimos
def render_extra_section(parent_frame, palabra):
    sinonimos = palabra["sinonimos"]
    if sinonimos:
        Label(parent_frame, text = "Sinónimos:").pack(anchor="w")
        for sinonimo in sinonimos:
            Label(parent_frame, text = f"- {sinonimo}").pack(anchor="w")
# Vuelve a los filtros del vocabulario.
# Se tendrá que pasar como parámetro la función y el callback
def go_back_to_vocab():
    estado["start_vocab_callback"]()
