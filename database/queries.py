from database import db


# Aquí estarán todas las funciones que consultan la BBDD

# --- FUNCIONES DE DASHBOARD ---

# devuelve el número total de palabras en vocabulario
def contar_total_palabras():
    res = db.fetch_one("SELECT COUNT(*) FROM vocabulario")
    return res[0]

# decuelve algo tipo: A1: 300 \nA2: 500 ...
def contar_palabras_por_nivel():
    p_por_nivel = db.fetch_all("SELECT nivel, COUNT(*) AS total FROM vocabulario GROUP BY nivel ORDER BY nivel")
    return[dict(fila) for fila in p_por_nivel]
# devuelve algo como noun: 800\nverb: 700 ...
def contar_palabras_por_tipo():
    p_por_tipo = db.fetch_all("SELECT tipo, COUNT(*) AS total FROM vocabulario GROUP BY tipo ORDER BY tipo")
    return[dict(fila) for fila in p_por_tipo]
# cuenta ejemplos en la tabla de ejemplos
def contar_total_ejemplos():
    res = db.fetch_one("SELECT COUNT(*) FROM ejemplos")
    return res[0]

# cuenta tags diponibles
def contar_total_tags():
    res = db.fetch_one("SELECT COUNT(*) FROM tags")
    return res[0]

# devuelve los tags más frecuentes según vocabulario_tags:
def obtener_tags_mas_usados(limite=10):
    pass

# funciones de filtros

def obtener_niveles_disponibles():
    niveles = db.fetch_all("SELECT nivel FROM vocabulario GROUP BY nivel ORDER BY nivel")
    return [dict(fila) for fila in niveles] # convertimos a diccionario

def obtener_tipos_disponibles():
    tipos =  db.fetch_all("SELECT tipo FROM vocabulario GROUP BY tipo ORDER BY tipo")
    return [dict(fila) for fila in tipos]

def obtener_tags_disponibles():
    tags = db.fetch_all("SELECT nombre FROM tags ORDER BY nombre")
    return [dict(fila) for fila in tags]

# --- FUNCIONES DE VOCABULARIO ---

def buscar_vocabulario(filtros):
    
    # query
    query = "SELECT DISTINCT vocabulario.* FROM vocabulario"
    params = []
    if filtros["tags"]:
        query += " JOIN vocabulario_tags ON vocabulario.id = vocabulario_tags.vocabulario_id JOIN tags ON tags.id = vocabulario_tags.tag_id WHERE tags.nombre IN ("
        for index, tag in enumerate(filtros["tags"]):
            query += "?"
            params.append(tag)
            if index != len(filtros["tags"])-1:
                query += ", "
        query += ")"

    if not filtros["tags"] and (filtros["tipos"] or filtros["niveles"]):
        query += " WHERE"
    if filtros["niveles"]:
        if filtros["tags"]:
            query += " AND"
        query += " nivel IN ("
        for index, nivel in enumerate(filtros["niveles"]):
            query += "?"
            params.append(nivel)
            if index != len(filtros["niveles"])-1:
                query += ", "
        query += ")"
    if filtros["tipos"]:
        if filtros["niveles"] or filtros["tags"]:
            query += " AND"
        query += " tipo IN ("
        for index, tipo in enumerate(filtros["tipos"]):
            query += "?"
            params.append(tipo)
            if index != len(filtros["tipos"])-1:
                query += ", "
        query += ")"
    if filtros["orden"] is not None:
        if filtros["orden"] == "random":
            query += " ORDER BY RANDOM()" 
        elif filtros["orden"] == "tags":
            query += " ORDER BY tags.nombre"
        else:
            query += " ORDER BY vocabulario." + filtros["orden"] 
    if str(filtros["limite"]).isdigit():
        query += " LIMIT ?"
        params.append(filtros["limite"])
    filas = db.fetch_all(query,params) 
    return [dict(fila) for fila in filas] # devolvemos una lista de diccionarios
    #return query, params

def obtener_vocabulario_por_id(vocabulario_id):
    fila = db.fetch_one("SELECT * FROM vocabulario WHERE id = ?",[vocabulario_id])
    if fila is None:
        return None
    return dict(fila)

def obtener_significados(vocabulario_id):
    significados = db.fetch_all("SELECT significado FROM significados WHERE vocabulario_id = ?",[vocabulario_id])
    return [fila["significado"] for fila in significados]

def obtener_ejemplos(vocabulario_id):
    ejemplos = db.fetch_all("SELECT ejemplo_de, ejemplo_es FROM ejemplos WHERE vocabulario_id = ?",[vocabulario_id])
    return [dict(fila) for fila in ejemplos]

def obtener_sinonimos(vocabulario_id):
    sinonimos = db.fetch_all("SELECT sinonimo FROM sinonimos WHERE vocabulario_id = ?",[vocabulario_id])
    return [fila["sinonimo"] for fila in sinonimos]

def obtener_tags_de_palabra(vocabulario_id): 
    tags = db.fetch_all("SELECT tags.nombre FROM vocabulario_tags JOIN tags ON vocabulario_tags.tag_id = tags.id WHERE vocabulario_tags.vocabulario_id = ?",[vocabulario_id])
    return [fila["nombre"] for fila in tags]

def obtener_vocabulario_completo(vocabulario_id):
    datos = obtener_vocabulario_por_id(vocabulario_id)
    if datos is None:
        return None
    return {
            "datos": datos,
            "significados": obtener_significados(vocabulario_id),
            "ejemplos": obtener_ejemplos(vocabulario_id),
            "sinonimos": obtener_sinonimos(vocabulario_id),
            "tags": obtener_tags_de_palabra(vocabulario_id)
            }

def obtener_lista_vocabulario_completo(filtros):
    vocab_list = buscar_vocabulario(filtros)
    palab_list = []
    for palabra in vocab_list:
        palab_list.append(obtener_vocabulario_completo(palabra["id"]))
    return palab_list

if __name__ == "__main__":
    print("Total palabras: ", contar_total_palabras())
    print("Total ejemplos: ", contar_total_ejemplos())
    print("Total tags: ", contar_total_tags())
    print("Palabras por nivel:")
    p_nivel = contar_palabras_por_nivel()
    for nivel in p_nivel:
        print("\t" + nivel["nivel"] + ": " + str(nivel["total"]))
    print("Palabras por tipo:")
    p_tipo = contar_palabras_por_tipo()
    for tipo in p_tipo:
        print("\t" + tipo["tipo"] + ": " + str(tipo["total"]))

    #print(obtener_niveles_disponibles())
    #print(obtener_tipos_disponibles())
    #print(obtener_tags_disponibles())

    filtros = {
            "niveles":[],  # "A2", "B1"
            "tipos":["noun","verb","adj"], # "noun", "verb"
            "tags":[], # "trabajo", "viajes"
            "limite":5, # podemos poner por ejemplo 20
            "orden":"random" # puede ser random, en base a la palabra, tags, tipos, etc. 
            }
    #res = buscar_vocabulario(filtros)
    #for r in res:
    #    print(r)
    print(obtener_vocabulario_por_id("v_neugierig"))
    print(obtener_significados("v_neugierig"))
    print(obtener_ejemplos("v_neugierig"))
    print(obtener_sinonimos("v_neugierig"))
    print(obtener_tags_de_palabra("v_neugierig"))

    print(obtener_vocabulario_completo("v_neugierig"))

    lista = obtener_lista_vocabulario_completo(filtros)
    for elem in lista:
        print(elem)
