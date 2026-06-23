# Script para comprobar que la tabla de progreso está vacía o tiene datos
# Contaremos las filas en vocabulario_progreso
# Contaremos resultados en ejercicio_resultados
# Mostraremos resumen por consola
# Es una forma rápida de ver si el progreso se está guardando
from database import db


def contar_progreso():
    # necesitamos acceder a la tabla vocabulario_progreso y mirar solo la cantidad de filas que hay
    total_progreso = db.fetch_one("SELECT COUNT(*) FROM vocabulario_progreso")
    return total_progreso[0]

def contar_resultados_ejercicios():
    # necesitamos acceder a ejercicio_resultados y ver la cantidad de filas que hay 
    total_ejercicios = db.fetch_one("SELECT COUNT(*) FROM ejercicio_resultados")
    return total_ejercicios[0]

def obtener_resumen():
    # Llamaremos a contar_progreso y contar_resultados_ejercicios y mostraremos el resumen con el formato indicado abajo. 
    progreso = contar_progreso()
    ejercicios = contar_resultados_ejercicios()
    return{"progreso":progreso, "ejercicios":ejercicios}

def mostrar_resumen():
    resumen = obtener_resumen()
    print(f"Filas en vocabulario_progreso: {resumen['progreso']}")
    print(f"Resultados de ejercicios: {resumen['ejercicios']}")
if __name__ == "__main__":
    mostrar_resumen()

# resultado esperado: 
# Filas en vocabulario_progreso: 0
# Resultados de ejercicios: 0


