import re

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

if __name__ == "__main__":
    #texto = "Geschäftsidee"
    texto = "sich kümmern um"
    #texto = "in Bezug auf"
    print(generar_id_base(texto))
