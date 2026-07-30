import re
from database import queries

# Limpia la palabra (un solo espacio, quitar signos raros, minúsculas)
def normalizar_para_id(texto):
    # quitamos espacios del principio y final
    texto = texto.lower().strip()
    # sustituimos los espacios múltiples por uno solo
    texto = re.sub(r"\s+"," ", texto)
    # eliminamos los símbolos raros
    texto = re.sub(r"[^a-züäöß\s]","", texto)
    return texto

# Genera el id de la BBDD a partir de una palabra dada
def generar_id_base(palabra):
    palabra = normalizar_para_id(palabra)
    dic_replace = {
            "ä":"ae",
            "ö":"oe",
            "ü":"ue",
            "ß":"ss",
            " ":"_"
            }
    # comprobamos si tiene algún caracter para sustituir y sustituimos
    for car,sus in dic_replace.items():
        palabra = palabra.replace(car,sus)
    return("v_" + palabra)

def generar_id_disponible(palabra):
    """ 
    Genera un ID disponible para una palabra
    - si v_umfahren no existe -> v_umfahren
    - si v_umfahren existe -> v_umfahren_2
    - si v_umfahren existe -> v_umfahren_3
    """
    id_provisional = generar_id_base(palabra)
    # si no existe lo devolvemos
    if not queries.existe_vocabulario_id(id_provisional):
        return id_provisional

    i = 2
    # si existe, le añadimos _X hasta que haya uno que no exista
    while queries.existe_vocabulario_id(f"{id_provisional}_{i}"):
        i += 1
    return f"{id_provisional}_{i}"


if __name__ == "__main__":
    #texto = "Geschäftsidee"
    texto = "sich kümmern um"
    #texto = "in Bezug auf"
    print(generar_id_base(texto))
    palabra = "Menge"

    print(generar_id_disponible(palabra))
    print(generar_id_disponible(texto))
