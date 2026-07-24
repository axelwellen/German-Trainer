from tkinter import *
# Pantalla del editor de vocabulario
from database import edit_queries, queries

def render_word_editor(parent_frame,vocabulario_id, on_save, on_cancel):
    # borrar el parent_frame que nos pasan
    for widget in parent_frame.winfo_children():
        widget.destroy()
    # obtener toda la información de la palabra
    palabra_completa = queries.obtener_vocabulario_completo(vocabulario_id)
    
    # Estado del editor que guarda referencias a los widgets que luego leeremos al pulsar guardad
    editor_state = {
            "palabra_completa": palabra_completa, 
            "basic_vars": {},
            "notas_widget": None, 
            "significados_entries": [], 
            "ejemplos_widgets": [],
            "sinonimos_entries": [],
            "tags_entries": []
            }
    # main frame
    main_frame = Frame(parent_frame)
    main_frame.pack(fill="both", expand = True, padx = 20, pady = 20)

    render_header(main_frame, palabra_completa)
    render_body(main_frame, editor_state)
    render_buttons(main_frame, editor_state, vocabulario_id, on_save, on_cancel)

def save(editor_state, vocabulario_id, on_save):
    
    palabra_completa = editor_state["palabra_completa"]
    datos = palabra_completa["datos"]
    basic_vars = editor_state["basic_vars"]
    

    datos["palabra"] = basic_vars["palabra"].get().strip()
    datos["tipo"] = basic_vars["tipo"].get().strip()
    datos["nivel"] = basic_vars["nivel"].get().strip()
    datos["genero"] = basic_vars["genero"].get().strip() or None # por si está vacío el campo guardar un NULL en SQLite
    
    datos["plural"] = basic_vars["plural"].get().strip()
    datos["preterito"] = basic_vars["preterito"].get().strip()
    datos["perfekt"] = basic_vars["perfekt"].get().strip()
    datos["auxiliar"] = basic_vars["auxiliar"].get().strip()
    datos["preposicion"] = basic_vars["preposicion"].get().strip()
    datos["caso"] = basic_vars["caso"].get().strip()
    
    datos["reflexivo"] = basic_vars["reflexivo"].get()
    datos["separable"] = basic_vars["separable"].get()
    
    # notas
    datos["notas"] = editor_state["notas_widget"].get("1.0", "end").strip() or None
    
    # significados
    significados = []
    for entry in editor_state["significados_entries"]:
        texto = entry.get().strip() # recuperamos el contenido 
        if texto:
            significados.append(texto)
    palabra_completa["significados"] = significados
    
    # sinonimos
    sinonimos = []
    for entry in editor_state["sinonimos_entries"]:
        texto = entry.get().strip()
        if texto:
            sinonimos.append(texto)
    palabra_completa["sinonimos"] = sinonimos

    # ejemplos
    ejemplos = []
    for ejemplo_widgets in editor_state["ejemplos_widgets"]:
        ejemplo_de = ejemplo_widgets["ejemplo_de"].get().strip()
        ejemplo_es = ejemplo_widgets["ejemplo_es"].get().strip()

        if ejemplo_de or ejemplo_es:
            ejemplos.append({
                "ejemplo_de": ejemplo_de, 
                "ejemplo_es": ejemplo_es
                })
    palabra_completa["ejemplos"] = ejemplos
    
    edit_queries.guardar_vocabulario_completo(vocabulario_id, palabra_completa)
    # llama a on_save que es actualizar_palabra_editada dentro de flashcard
    on_save(vocabulario_id)


def render_header(parent_frame, palabra_completa):
    header_frame = Frame(parent_frame)
    header_frame.pack(anchor = "w", padx = 20, pady = 10)
    # titulo
    Label(header_frame, text = "Editor").pack(anchor = "w", pady = 10)
    Label(header_frame, text = f"Editar palabra: {palabra_completa['datos']['palabra']}").pack(anchor = "w", pady = 10)
        
def render_body(parent_frame, editor_state):
    
    palabra_completa = editor_state["palabra_completa"]

    body_frame = Frame(parent_frame)
    body_frame.pack(anchor = "w", padx = 20, pady = 10, fill="x")
    
    # configuramos dos columnas princpales
    body_frame.columnconfigure(0, weight = 1)
    body_frame.columnconfigure(1, weight = 1)

    datos_frame = LabelFrame(body_frame, text="Datos básicos", padx = 10, pady = 10)
    notas_frame = LabelFrame(body_frame, text="Notas",padx = 10, pady = 10)

    datos_frame.grid(row=0, column = 0, sticky = "nsew", padx = 10, pady = 10)
    notas_frame.grid(row=0, column = 1, sticky = "nsew", padx = 10, pady = 10)

    render_datos_basicos(datos_frame, editor_state, palabra_completa["datos"])
    render_notas(notas_frame, editor_state, palabra_completa["datos"])
    
    significados_frame = LabelFrame(body_frame, text = "Significados", padx = 10, pady = 10)
    significados_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 10)

    render_significados(significados_frame, editor_state, palabra_completa["significados"])

    sinonimos_frame = LabelFrame(body_frame, text = "Sinónimos", padx = 10, pady = 10)
    sinonimos_frame.grid(row = 2, column = 0, sticky = "nsew", padx = 10, pady = 10)

    render_sinonimos(sinonimos_frame, editor_state, palabra_completa["sinonimos"])

    ejemplos_frame = LabelFrame(body_frame, text = "Ejemplos", padx = 10, pady = 10)
    ejemplos_frame.grid(row = 1, column = 1, sticky = "nsew", padx = 10, pady = 10)

    render_ejemplos(ejemplos_frame, editor_state, palabra_completa["ejemplos"])

def crear_entry(parent, label_text, value, row, column, width=18, disabled = False):
    Label(parent, text=label_text).grid(row=row, column = column, sticky = "w", padx = 5, pady = (5,0))
    entry = Entry(parent, width=width)
    entry.insert(0, value or "")
    if disabled:
        entry.config(state="disabled")
    entry.grid(row = row +1, column = column, sticky = "ew", padx = 5, pady = (0,8))
    return entry

def render_datos_basicos(parent_frame, editor_state, datos):
    parent_frame.columnconfigure(0,weight=1)
    parent_frame.columnconfigure(1,weight=1)
    parent_frame.columnconfigure(2,weight=1)
    parent_frame.columnconfigure(3,weight=1)
    
    basic_vars = editor_state["basic_vars"]

    # id
    basic_vars["id"] = crear_entry(parent_frame, "ID", datos["id"], 0,0, disabled = True)
    
    # palabra
    # Guarda la referencia al widget Entry. Apunta al propio campo de Tkinter. 
    # Al hacer editor_state["basic_vars"]["palabra"].get() obtenemos el contenido del campo
    basic_vars["palabra"] = crear_entry(parent_frame, "Palabra", datos["palabra"], 0,1)

    # Tipo
    basic_vars["tipo"] = crear_entry(parent_frame, "Tipo", datos["tipo"], 0,2)

    # nivel
    basic_vars["nivel"] = crear_entry(parent_frame, "Nivel", datos["nivel"], 0,3)

    # género
    basic_vars["genero"] = crear_entry(parent_frame, "Género", datos["genero"], 2,0)
    
    # plural
    basic_vars["plural"] = crear_entry(parent_frame, "Plural", datos["plural"], 2,1)
    
    # preterito
    basic_vars["preterito"] = crear_entry(parent_frame, "Pretérito", datos["preterito"], 2,2)
    
    # perfekt
    basic_vars["perfekt"] = crear_entry(parent_frame, "Perfekt", datos["perfekt"], 2,3)
    
    # auxiliar
    basic_vars["auxiliar"] = crear_entry(parent_frame, "Auxiliar", datos["auxiliar"], 4,0)
    
    # preposición
    basic_vars["preposicion"] = crear_entry(parent_frame, "Preposición", datos["preposicion"], 4,1)
    
    # caso
    basic_vars["caso"] = crear_entry(parent_frame, "Caso", datos["caso"], 4,2)
    
    reflexivo_var = IntVar(value=datos["reflexivo"] or 0)
    separable_var = IntVar(value=datos["separable"] or 0)

    Checkbutton(parent_frame, text="Reflexivo", variable = reflexivo_var).grid(row=6, column = 0, sticky = "w", padx = 5, pady = 5)
    Checkbutton(parent_frame, text="Separable", variable = separable_var).grid(row=6, column = 1, sticky = "w", padx = 5, pady = 5)

    basic_vars["reflexivo"] = reflexivo_var
    basic_vars["separable"] = separable_var

# Usaremos Text con las notas, no Entry
def render_notas(parent_frame, editor_state, datos):
    notas_text = Text(parent_frame, height=12, width=45, wrap="word")
    notas_text.insert("1.0", datos["notas"] or "")
    notas_text.pack(fill="both", expand=True, padx = 5, pady = 5)
    
    editor_state["notas_widget"] =  notas_text


def render_significados(parent_frame, editor_state, significados):
    rows_frame = Frame(parent_frame)
    rows_frame.pack(fill="x", expand = True)

    editor_state["significados_entries"] = []
    
    # recorremos cada significado de la lista que tenemos en la palabra completa
    for significado in significados: 
        # por cada significado creamos un Entry
        add_significado_row(rows_frame, editor_state, significado)
    
    # incluimos un botón abajo que nos crea un nuevo Entry vacío
    Button(parent_frame, text = "+ Añadir significado", command = lambda: add_significado_row(rows_frame, editor_state, "")).pack(anchor="w", pady=5)

def render_sinonimos(parent_frame, editor_state, sinonimos):
    rows_frame = Frame(parent_frame)
    rows_frame.pack(fill="x", expand=True)
 
    editor_state["sinonimos_entries"] = []
    
    # recorremos cada sinonimo de la lista que tenemos en la palabra completa
    for sinonimo in sinonimos: 
        # por cada significado creamos un Entry
        add_sinonimo_row(rows_frame, editor_state, sinonimo)
    
    # incluimos un botón abajo que nos crea un nuevo Entry vacío
    Button(parent_frame, text = "+ Añadir sinónimo", command = lambda: add_sinonimo_row(rows_frame, editor_state, "")).pack(anchor="w", pady=5)

def render_ejemplos(parent_frame, editor_state, ejemplos):
    rows_frame = Frame(parent_frame)
    rows_frame.pack(fill="both", expand=True)
 
    editor_state["ejemplos_widgets"] = []
    
    # recorremos cada par de ejemplos de la lista que tenemos en la palabra completa
    for ejemplo in ejemplos: 
        # por cada ejemplo creamos un par de entrys
        add_ejemplos_row(rows_frame, editor_state, ejemplo)
    
    # incluimos un botón abajo que nos crea un nuevo Entry vacío
    Button(parent_frame, text = "+ Ejemplo", command = lambda: add_ejemplos_row(rows_frame, editor_state)).pack(anchor="w", pady=5)

def add_ejemplos_row(parent_frame, editor_state, valor = None):
    if valor is None:
        valor = {
                "ejemplo_de" : "",
                "ejemplo_es" : ""
                }
    ejemplo_frame = LabelFrame(parent_frame, padx = 10, pady = 10)
    ejemplo_frame.pack(fill = "x", expand = True, pady = 5)
    
    Label(ejemplo_frame, text = "Alemán").pack(anchor="w")

    entry_de = Entry(ejemplo_frame)
    entry_de.insert(0,valor["ejemplo_de"] or "")
    entry_de.pack(fill="x", expand = True, pady = (0,5))
    
    Label(ejemplo_frame, text = "Español").pack(anchor="w")

    entry_es = Entry(ejemplo_frame)
    entry_es.insert(0, valor["ejemplo_es"] or "")
    entry_es.pack(fill="x", expand = True, pady = (0,5))
    
    ejemplo_widgets = {
            "frame": ejemplo_frame,
            "ejemplo_de": entry_de, 
            "ejemplo_es": entry_es
            }
    editor_state["ejemplos_widgets"].append(ejemplo_widgets)

    # Creamos el botón para eliminar las Entrys
    Button(ejemplo_frame, text = "X", command = lambda: eliminar_ejemplo_row(ejemplo_widgets, editor_state)).pack(anchor="e")

def add_significado_row(parent_frame, editor_state, valor = ""):
    row_frame = Frame(parent_frame)
    row_frame.pack(fill="x", pady = 2)

    # Creamos un entry vacío
    entry = Entry(row_frame)
    entry.insert(0, valor or "")
    entry.pack(side="left", fill="x", expand = True, padx = (0,5))
    
    # agregamos la referencia de entry al editor_state
    editor_state["significados_entries"].append(entry)

    # Creamos el botón para elminar el Enty, llama a eliminar_significado_row
    Button(row_frame, text="X", command=lambda: eliminar_significado_row(row_frame, entry, editor_state)).pack(side="left")

def add_sinonimo_row(parent_frame, editor_state, valor = ""):
    row_frame = Frame(parent_frame)
    row_frame.pack(fill="x", pady=2)

    # Creamos un entry vacío
    entry = Entry(row_frame)
    entry.insert(0, valor or "")
    entry.pack(side="left", fill="x", expand = True, padx = (0,5))

    # agregamos la referencia de entry al editor_state
    editor_state["sinonimos_entries"].append(entry)

    # Creamos el botón para eliminar el Entry, llama a eliminar_sinonimo_row
    Button(row_frame, text = "X", command = lambda: eliminar_sinonimo_row(row_frame, entry, editor_state)).pack(side="left")

def eliminar_significado_row(parent_frame, entry, editor_state):
    if entry in editor_state["significados_entries"]:
        # eliminamos el significado en caso de que estuviera en el editor_state
        editor_state["significados_entries"].remove(entry)
    parent_frame.destroy()

def eliminar_sinonimo_row(parent_frame, entry, editor_state):
    if entry in editor_state["sinonimos_entries"]:
        # eliminamos el significado en caso de que estuviera en el editor_state
        editor_state["sinonimos_entries"].remove(entry)
    parent_frame.destroy()  

def eliminar_ejemplo_row(ejemplo_widgets, editor_state):
    if ejemplo_widgets in editor_state["ejemplos_widgets"]:
        editor_state["ejemplos_widgets"].remove(ejemplo_widgets)
    ejemplo_widgets["frame"].destroy()

def render_buttons(parent_frame, editor_state, vocabulario_id, on_save, on_cancel):
    
    botones_frame = Frame(parent_frame)
    botones_frame.pack(anchor = "center", pady = 10)

    Button(botones_frame, text = "Guardar", command = lambda: save(editor_state, vocabulario_id, on_save)).pack(side="left", padx=5)

    Button(botones_frame, text = "Cancelar", command =on_cancel).pack(side="left", padx=5)

   


