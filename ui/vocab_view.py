from database import queries
from tkinter import *

# veremos los filtros para generar la lista de vocabulario para estudiar
estado = {
        "nivel_vars": {},
        "tipo_vars": {},
        "tag_vars": {},
        "limite_var":None,
        "orden":"random",
        "start_flashcards_callback": None
        }

def render_vocab_view(parent_frame, start_flashcards_callback):
    estado["start_flashcards_callback"] = start_flashcards_callback # guardamos la función como objeto
    # titulo
    Label(parent_frame, text="Vocabulario").pack(anchor = "w", pady = 10)

    # filtros frame
    filters_frame = Frame(parent_frame)
    filters_frame.pack(anchor = "w", padx = 20, pady = 10)
    render_filters(filters_frame)

    # botones_frame
    buttons_frame = Frame(parent_frame)
    buttons_frame.pack(anchor = "center")
    render_botones(buttons_frame)

    # resultados_frame
    resultados_frame = Frame(parent_frame)
    resultados_frame.pack(anchor = "w", padx = 20, pady = 10)
    
    # detalle_frame
    detalle_frame = Frame(parent_frame)
    detalle_frame.pack(anchor = "w", padx = 20, pady = 10)

def render_filters(filters_frame):
    niveles = queries.obtener_niveles_disponibles()
    tipos = queries.obtener_tipos_disponibles()
    tags = queries.obtener_tags_disponibles()
    
    # NIVELES
    nivel_frame = Frame(filters_frame)
    nivel_frame.pack(anchor="w", padx = 20, pady = 10)
    Label(nivel_frame, text="Nivel:").grid(row=0, column=0, sticky="w")
    for i,item in enumerate(niveles): 
        nivel = item["nivel"]
        var = IntVar()
        estado["nivel_vars"][nivel] = var # es una variable que puede valer 0 a 1 según el get

        Checkbutton(nivel_frame, text=nivel, variable=var).grid(row=1, column = i, sticky="w", padx = 5)
    # TIPOS
    tipo_frame = Frame(filters_frame)
    tipo_frame.pack(anchor="w", padx = 20, pady = 10)
    Label(tipo_frame, text="Tipo:").grid(row=0, column=0, sticky="w")
    for i,item in enumerate(tipos):
        tipo = item["tipo"]
        var = IntVar()
        estado["tipo_vars"][tipo] = var

        Checkbutton(tipo_frame, text=tipo, variable=var).grid(row=1, column = i, sticky = "w", padx = 5)
    # TAGS
    tags_frame = Frame(filters_frame)
    tags_frame.pack(anchor="w", padx=20, pady=10)
    Label(tags_frame, text="Tags:").grid(row=0, column=0, sticky="w")
    columnas = 7
    for i,item in enumerate(tags):
        tag = item["nombre"]
        var = IntVar()
        estado["tag_vars"][tag] = var
        fila = (i//columnas) +1#
        columna = i % columnas
        Checkbutton(tags_frame, text=tag, variable=var).grid(row = fila, column = columna, sticky = "w", padx = 5, pady=2)
    # LIMITE
    lim_frame = Frame(filters_frame)
    lim_frame.pack(anchor="w", padx=20, pady = 10)
    Label(lim_frame, text="Límite de palabras").grid(row=0, column = 0, sticky = "w")
    estado["limite_var"] = StringVar(value="20")
    entry = Entry(lim_frame, textvariable=estado["limite_var"])
    entry.grid(row=0, column=1, sticky = "w")

def render_botones(buttons_frame):
    # botón cargar palabras
    btn_cargar = Button(buttons_frame, text="Cargar palabras", command = load_words)
    btn_cargar.config(width = 15, height = 2)
    btn_cargar.pack(side="left", padx = 2, pady = 5)
    # botón limpiar filtros
    btn_limpiar = Button(buttons_frame, text="Limpiar filtros", command = clear_filters)
    btn_limpiar.config(width = 15, height = 2)
    btn_limpiar.pack(side="left", padx = 2, pady = 5)
    # botón estudiar con tarjetas
    btn_estudiar = Button(buttons_frame, text="Estudiar Vocabulario", command = start_flashcards)
    btn_estudiar.config(width = 15, height = 2)
    btn_estudiar.pack(side="left", padx = 2, pady = 5)

# lee los checkbuttons seleccionados y devuelve
# {niveles:["B1","B2"], tipos:["noun","verb"], ... lo que necesitamos para crear el filtro
def get_selected_filters():
    niveles = []
    tipos = []
    tags = []
    for nivel, var in estado["nivel_vars"].items():
        if var.get() == 1:
            niveles.append(nivel)
    for tipo, var in estado["tipo_vars"].items():
        if var.get() == 1:
            tipos.append(tipo)
    for tag, var in estado["tag_vars"].items():
        if var.get() == 1:
            tags.append(tag)
    try: 
        limite = int(estado["limite_var"].get())
    except ValueError:
        limite = 20
    return {
            "niveles":niveles, # ["A2", "B1"]
            "tipos": tipos, # ["noun", "verb"]
            "tags": tags, # ["trabajo", "viajes"]
            "limite": limite, # 20
            "orden": estado["orden"] # puede ser tags, palabra, random, etc
            }

# usa get_selected_filters() y llama a cargar_vocabulario_para_estudio(filtros):
def load_words(filtros=None):
    if filtros is None:
        filtros = get_selected_filters()
    lista_vocab = queries.obtener_lista_vocabulario_completo(filtros)
    print(lista_vocab)
    print(f"Palabras cargadas: {len(lista_vocab)}")
    return lista_vocab
# para el MVP no lo haré
# muestra resultados en tabla/lista
def render_word_list(palabras):
    pass

# para el MVP no lo haré
# al hacer clic en una palabra muestra:
# significados, notas, ejemplos, tags, género/plural, datos verbales...
def show_word_detail(vocab_item):
    pass

# desmarca todo y deja valores por defecto
def clear_filters():
    for nivel, var in estado["nivel_vars"].items():
        var.set(0)
    for tipo, var in estado["tipo_vars"].items():
        var.set(0)
    for tag, var in estado["tag_vars"].items():
        var.set(0)
    if estado["limite_var"] is not None:
        estado["limite_var"].set("20")

# si hay palabras cargadas, abre FlashcardView
def start_flashcards():
    filtros = get_selected_filters()
    palabras = load_words(filtros)
    if len(palabras) == 0:
        print("No hay palabras con estos filtros")
        return
    estado["start_flashcards_callback"](palabras) # ejecutamos la función pasada como parametro, es como hacer show_flashcards(palabras)

