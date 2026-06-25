from database import progress_queries as progress_q

# El objetivo de estas funciones es poderlas utilizar sin usar la base de datos. (calcular_nuevo_peso, calcular_estado)

# devuelve el nuevo peso en base al peso_actual de la palabra y a la nueva valoración que le hemos dado
def calcular_nuevo_peso(peso_actual, valoracion):
    if valoracion == 1:
        nuevo = peso_actual * 1.60
    elif valoracion == 2:
        nuevo = peso_actual * 1.15
    elif valoracion == 3:
        nuevo = peso_actual * 0.75
    elif valoracion == 4:
        nuevo = peso_actual * 0.45
    else: 
        nuevo = peso_actual

    return max(0.1, min(nuevo,5.00)) # acotamos los valores entre 0.1 y 5

# valcula el nuevo estado de la palabra en base al peso que tiene y a las veces que la hemos visto
def calcular_estado(peso_repaso, veces_vista):
    if veces_vista <= 0:
        return "nueva"
    if peso_repaso >= 3.0:
        return "difícil"
    if peso_repaso <= 0.5:
        return "dominada"
    return "aprendiendo"

# no es necesaria por el momento 
def normalizar_valoracion(valoracion):
    pass

# crea progreso si no existe 
# lee progreso actual
# actualiza:  veces vista, valoracion ultima, aciertos/fallos, peso_repaso, estado, utlima vez 
# esta función debería funcionar para primera vez y para repaso. La diferencia está en el modo con el que llega. modo = estudio, modo = repaso, por ejemplo. 
def actualizar_progreso_por_valoracion(vocabulario_id, valoracion, modo = "flashcard"):
    # creamos progreso si no existe
    if not progress_q.existe_progreso(vocabulario_id):
        progress_q.crear_progreso_inicial(vocabulario_id)
    # obtenemos progreso
    progreso = progress_q.obtener_progreso(vocabulario_id)
    # actualizamos veces_vista
    progreso["veces_vista"] += 1
    if modo in ["repaso", "ejercicio"]:
        progreso["veces_repasada"] += 1
    # actualizamos valoracion_ultima
    progreso["valoracion_ultima"] = valoracion
    # actualizar aciertos/fallos
    # en caso de valorar, no contamos como acierto ni fallo
    # recalcular peso_repaso
    progreso["peso_repaso"] = calcular_nuevo_peso(progreso["peso_repaso"], valoracion)
    # recalcular estado
    progreso["estado"] = calcular_estado(progreso["peso_repaso"], progreso["veces_vista"])
    # actualizar_progreso
    progress_q.actualizar_progreso(progreso)
    
    return progreso


if __name__ == "__main__":
    print(calcular_nuevo_peso(3.5,1))
    print(calcular_nuevo_peso(4.8,4))
    print(calcular_nuevo_peso(3,2))
    print(calcular_nuevo_peso(1,3))
    print(calcular_nuevo_peso(5,2))
    print(calcular_estado(3,7))
    print(calcular_estado(3,0))
    print(calcular_estado(5,2))
    print(calcular_estado(0.2,2))
    print(calcular_estado(2,5))
    progreso = actualizar_progreso_por_valoracion("v_hi", 1)
    print(progreso)
