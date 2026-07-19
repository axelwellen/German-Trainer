from database import queries
from database import db
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

if __name__ == "__main__":
    vocabulario_id = "v_aufessen"
    datos_completos = queries.obtener_vocabulario_completo(vocabulario_id)
    print(datos_completos)
    datos_completos["datos"]["preterito"] = "aß auf"
    print(datos_completos)
    datos_completos["datos"]["perfekt"] = "aufgegessen"
    datos_completos["datos"]["auxiliar"] = "haben"
    actualizar_vocabulario_basico(vocabulario_id, datos_completos["datos"])
    print("campos actualizados")
    
    datos_completos = queries.obtener_vocabulario_completo(vocabulario_id)
    print(datos_completos)
