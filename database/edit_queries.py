from database import queries
from database import db
from services import id_service

# actualiza la tabla de vocabulario a partir del id y de los datos que teníamos. 
# Debe existir el vocabulario_id, sino usaremos la función crear_vocabulario_básico
def actualizar_vocabulario_basico(vocabulario_id, datos):
    query = """
        UPDATE vocabulario
        SET palabra = ?,
            tipo = ?, 
            nivel = ?,
            notas = ?,
            genero = ?,
            plural = ?,
            preterito = ?,
            perfekt = ?,
            auxiliar = ?,
            reflexivo = ?,
            separable = ?,
            preposicion = ?,
            caso = ?
        WHERE id = ?
    """

    params = [
            datos["palabra"],
            datos["tipo"],
            datos["nivel"],
            datos["notas"],
            datos["genero"],
            datos["plural"],
            datos["preterito"],
            datos["perfekt"],
            datos["auxiliar"],
            datos["reflexivo"],
            datos["separable"],
            datos["preposicion"],
            datos["caso"],
            vocabulario_id,
        ]        

    db.execute_query(query,params)

def crear_vocabulario_basico(datos):
    """
        Esta función es similar a la de actualizar_vocabulario_basico(vocabulario_id, datos)
        Pero en este caso tendremos que llamar a la función generar_id_disponible de services/id_service
        Devuelve el id generado
    """
    query = "INSERT INTO vocabulario (id, palabra, tipo, nivel, notas, genero, plural, preterito, perfekt, auxiliar, reflexivo, separable, preposicion, caso) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    id_palabra = id_service.generar_id_disponible(datos["palabra"])
    params = [
            id_palabra,
            datos["palabra"],
            datos["tipo"],
            datos.get("nivel"),
            datos.get("notas"),
            datos.get("genero"),
            datos.get("plural"),
            datos.get("preterito"),
            datos.get("perfekt"),
            datos.get("auxiliar"),
            datos.get("reflexivo"),
            datos.get("separable"),
            datos.get("preposicion"),
            datos.get("caso"),   
        ]
    db.execute_query(query, params)
    return id_palabra

# Función para reemplazar los significados de una palabra
def reemplazar_significados(vocabulario_id, significados):
    # Query para eliminar los significados
    delete_query = "DELETE FROM significados WHERE vocabulario_id = ?"
    db.execute_query(delete_query, [vocabulario_id])
    
    # Query para insertar todos los significados
    insert_query = "INSERT INTO significados (vocabulario_id, significado) VALUES (?,?)"
    params = []
    for significado in significados:
        params.append((vocabulario_id, significado)) # creamos la tupla
    db.execute_many_query(insert_query, params)

def reemplazar_ejemplos(vocabulario_id, ejemplos):
    # Query para eliminar los ejemplos
    delete_query = "DELETE FROM ejemplos WHERE vocabulario_id = ?"
    db.execute_query(delete_query, [vocabulario_id])

    # Query para insertar todos los ejemplos
    insert_query = "INSERT INTO ejemplos (vocabulario_id, ejemplo_de, ejemplo_es) VALUES (?,?,?)"
    params = []
    for ejemplo in ejemplos:
        params.append((vocabulario_id, ejemplo["ejemplo_de"].strip(), ejemplo["ejemplo_es"].strip()))
    db.execute_many_query(insert_query, params)

def obtener_o_crear_tag(nombre_tag):
    # Query para buscar si existe el tag y obtener su id
    search_query = "SELECT * FROM tags WHERE nombre = ?"
    res = db.fetch_one(search_query,[nombre_tag])
    if res is not None:
        return res["id"]
    # Si no existe el tag, lo creamos y retornamos su id
    else: 
        insert_query = "INSERT INTO tags (nombre) VALUES (?)"
        db.execute_query(insert_query, [nombre_tag])
    res = db.fetch_one(search_query,[nombre_tag])
    return res["id"]

def reemplazar_tags(vocabulario_id, tags):
    # Query para eliminar todos los tags asociados a las palabras
    delete_query = "DELETE FROM vocabulario_tags WHERE vocabulario_id = ?"
    db.execute_query(delete_query,[vocabulario_id])

    # Obtener el id de cada tag y crear las relaciones en la tabla vocabulario_tags
    
    ids_tags = set()
    for tag in tags: 
        tag = tag.strip().lower() # limpiamos el tag
        if tag: 
            ids_tags.add(obtener_o_crear_tag(tag)) # conjunto para que no haya duplicados
    params = [(vocabulario_id,tag_id) for tag_id in list(ids_tags)]
    insert_query = "INSERT INTO vocabulario_tags (vocabulario_id, tag_id) VALUES (?,?)"
    db.execute_many_query(insert_query, params)

# Para la V02 no resolvemos los ids (pueden no existir), tenemos que escribir los ids como sinónimos. 
def reemplazar_sinonimos(vocabulario_id, sinonimos_ids):
    # Query para eliminar todos los sinónimos
    delete_query = "DELETE FROM sinonimos WHERE vocabulario_id = ?"
    db.execute_query(delete_query, [vocabulario_id])
    
    # Query para insertar la lista de sinónimos
    sinonimos_limpios = set()
    for sinonimo in sinonimos_ids:
        sinonimo = sinonimo.strip().lower()
        if sinonimo:
            sinonimos_limpios.add(sinonimo)

    params = [(vocabulario_id,sinonimo) for sinonimo in sinonimos_limpios] # evitamos duplicados y limpiamos
    insert_query = "INSERT INTO sinonimos (vocabulario_id, sinonimo) VALUES (?,?)"
    db.execute_many_query(insert_query, params) 

# la estructura es la que tenemos siempre, diccionario de: datos, significados, ejemplos, sinonimos, tags
def guardar_vocabulario_completo(vocabulario_id, vocabulario_completo):
    # llamamos a actualizar_vocabulario_basico
    actualizar_vocabulario_basico(vocabulario_id, vocabulario_completo["datos"])
    # llamamos a reemplazar significados
    reemplazar_significados(vocabulario_id, vocabulario_completo["significados"])
    # llamamos a reemplazar_ejemplos
    reemplazar_ejemplos(vocabulario_id, vocabulario_completo["ejemplos"])
    # llamamos a reemplazar tags
    reemplazar_tags(vocabulario_id, vocabulario_completo["tags"])
    # llamamos a reemplazar_sinonimos
    reemplazar_sinonimos(vocabulario_id, vocabulario_completo["sinonimos"])

def crear_vocabulario_completo(vocabulario_completo):
    """
        Función que añade una palabra a la BBDD a partir de todos sus datos
    """
    # llamamos a crear_vocabulario_basico():
    vocabulario_id = crear_vocabulario_basico(vocabulario_completo["datos"])
    vocabulario_completo["datos"]["id"] = vocabulario_id
    # llamamos a reemplazar significados
    reemplazar_significados(vocabulario_id, vocabulario_completo["significados"])
    # llamamos a reemplazar_ejemplos
    reemplazar_ejemplos(vocabulario_id, vocabulario_completo["ejemplos"])
    # llamamos a reemplazar tags
    reemplazar_tags(vocabulario_id, vocabulario_completo["tags"])
    # llamamos a reemplazar_sinonimos
    reemplazar_sinonimos(vocabulario_id, vocabulario_completo["sinonimos"])


if __name__ == "__main__":
#     vocabulario_id = "v_aufessen"
#     datos_completos = queries.obtener_vocabulario_completo(vocabulario_id)
#     print(datos_completos)
#     datos_completos["datos"]["preterito"] = "aß auf"
#     print(datos_completos)
#     datos_completos["datos"]["perfekt"] = "aufgegessen"
#     datos_completos["datos"]["auxiliar"] = "haben"
#     actualizar_vocabulario_basico(vocabulario_id, datos_completos["datos"])
#     print("campos actualizados")
#     
#     datos_completos = queries.obtener_vocabulario_completo(vocabulario_id)
#     print(datos_completos)
# 
#     print(queries.obtener_vocabulario_completo("v_beliebt"))
#     significados = ["popular","querido","apreciado","solicitado"]
#     reemplazar_significados("v_beliebt",significados)
#     print("Significados modificados")
#     print(queries.obtener_vocabulario_completo("v_beliebt"))
# 
#     ejemplos = [
#             {
#                 "ejemplo_de":"Der Zug fährt um 9:15 ab.",
#                 "ejemplo_es":"El tren sale a las 9:15"
#             },
#             {
#                 "ejemplo_de":"Unser Zug ist schon abgefahren",
#                 "ejemplo_es":"Nuestro tren ya ha salido"
#             }]
#     reemplazar_ejemplos("v_abfahren", ejemplos)
#     print("Ejemplos modificados")
#     print(queries.obtener_vocabulario_completo("v_abfahren"))
# 
#     print(obtener_o_crear_tag("amigos"))
#     tags=["alltag", "essen", "arbeit", "politik", "tiempo_libre"]
#     reemplazar_tags("v_neugierig", tags)
#     sinonimos = ["v_unantastbar"]
#     reemplazar_sinonimos("v_heilig", sinonimos)

    vocabulario_completo = {
            'datos': 
            {
                'id': 'v_aufessen',
                'palabra': 'aufessen', 
                'tipo': 'verb', 
                'nivel': 'B1', 
                'notas': '"Verbo separable: ich esse auf, du isst auf, er isst auf; Perfekt: hat aufgegessen."', 
                'genero': None, 
                'plural': None, 
                'preterito': "aß auf", 
                'perfekt': "aufgegessen", 
                'auxiliar': "haben", 
                'reflexivo': 0, 
                'separable': 1, 
                'preposicion': None, 
                'caso': None
                }, 
            'significados': ['comerse todo', 'terminar de comer', 'finalizar la comida'], 
            'ejemplos': [
                {
                    'ejemplo_de': 'Iss bitte deinen Teller auf!', 
                    'ejemplo_es': '¡Cómete todo el plato, por favor!'
                    },
                {
                    'ejemplo_de': 'Iss deine Suppe auf!',
                    'ejemplo_es': 'Termínate la sopa!'
                    }
                ], 
            'sinonimos': ["v_auffuttern","v_verzehren"], 
            'tags': ['alltag', 'essen', 'comida']
            }
    crear_vocabulario_completo(vocabulario_completo)

