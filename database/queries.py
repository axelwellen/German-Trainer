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

def obtener_modos_disponibles():
    modos = db.fetch_all("SELECT DISTINCT estado AS modo FROM vocabulario_progreso ORDER BY estado")
    return [dict(fila) for fila in modos]

# --- FUNCIONES DE VOCABULARIO ---

def existe_vocabulario_id(vocabulario_id):
    """ Función que devuelve True si existe el id en la BBDD o False si no existe """
    vocab = db.fetch_one("SELECT 1 FROM vocabulario WHERE id = ?",[vocabulario_id])
    return vocab is not None

def crear_placeholders(valores):
    return ", ".join(["?"] * len(valores))
    
def buscar_vocabulario(filtros):
    query = "SELECT DISTINCT v.* FROM vocabulario v"
    joins = []
    where = []
    params = []

    niveles = filtros.get("niveles",[])
    tipos = filtros.get("tipos",[])
    tags = filtros.get("tags",[])
    modo_progreso = filtros.get("modo_progreso", "todas")
    orden = filtros.get("orden",None)
    limite = filtros.get("limite",20)

    # TAGS
    if tags:
        joins.append("""
            JOIN vocabulario_tags vt ON v.id = vt.vocabulario_id
            JOIN tags t ON t.id = vt.tag_id
        """)
        placeholders = crear_placeholders(tags)
        where.append(f"t.nombre IN ({placeholders})")
        params.extend(tags)

    # PROGRESO
    if modo_progreso != "todas":
        joins.append("""
            LEFT JOIN vocabulario_progreso p ON v.id = p.vocabulario_id
        """)
        # palabras nunca estudiadas o con estado "nueva"
        if modo_progreso == "nuevas":
            where.append("(p.vocabulario_id IS NULL OR p.estado = 'nueva')")

        # palabras que ya tienen fila en vocabulario_progreso
        elif modo_progreso == "vistas":
            where.append("p.vocabulario_id IS NOT NULL")

        # palabras con estado aprendiendo
        elif modo_progreso == "aprendiendo":
            where.append("p.estado = 'aprendiendo'")
        
        # palabras con estado difíciles
        elif modo_progreso == "dificil":
            where.append("p.estado = 'dificil'")

        # palabras con estado dominadas
        elif modo_progreso == "dominada":
            where.append("p.estado = 'dominada'")

    # --- NIVELES ---
    if niveles:
        placeholders = crear_placeholders(niveles)
        where.append(f"v.nivel IN ({placeholders})")
        params.extend(niveles)

    # --- TIPOS ---
    if tipos:
        placeholders = crear_placeholders(tipos)
        where.append(f"v.tipo IN ({placeholders})")
        params.extend(tipos)

    # --- MONTAR QUERY ---
    if joins:
        query += " " + " ".join(joins)

    if where:
        query += " WHERE " + " AND ".join(where)

    # --- ORDEN ---
    if orden:
        if orden == "random":
            query += " ORDER BY RANDOM()"

        elif orden == "tags" and tags:
            query += " ORDER BY t.nombre"

        elif orden == "prioridad_repaso":
            if modo_progreso in ["vistas", "aprendiendo", "dificil", "dominada"]:
                query += " ORDER BY p.peso_repaso DESC"
            else:
                query += " ORDER BY RANDOM()"
        elif orden in ["palabra", "nivel", "tipo"]:
            query += f" ORDER BY v.{orden}"

    # --- LÍMITE ---
    if str(limite).isdigit():
        query += " LIMIT ?"
        params.append(int(limite))

    filas = db.fetch_all(query, params)
    return [dict(fila) for fila in filas]


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
    print(obtener_niveles_disponibles(),"esta es la función")
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
