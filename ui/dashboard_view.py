from database import queries
from tkinter import *
# muestra el dashboard cuando app.py lo llame

# pide datos a queries.py
def load_dashboard_data():
    return {
            "total_palabras": queries.contar_total_palabras(),
            "total_ejemplos": queries.contar_total_ejemplos(),
            "total_tags": queries.contar_total_tags(),
            "palabras_por_nivel": queries.contar_palabras_por_nivel(),
            "palabras_por_tipo": queries.contar_palabras_por_tipo()
            #"tags_mas_usados": queries.obtener_tags_mas_usados() no existe en el MVP
            }
# dibuja los datos en el frame que recibe.
def render_dashboard(parent_frame):
    datos = load_dashboard_data()
    
    # título
    Label(parent_frame, text="Dashboard").pack(anchor = "w", pady = 10)
    
    # resumen general
    resumen_frame = Frame(parent_frame)
    resumen_frame.pack(anchor="w", padx=20, pady=10)

    Label(resumen_frame, text="Resumen general:").pack(anchor="w")
    Label(resumen_frame, text=f"Total palabras: {datos['total_palabras']}").pack(anchor="w")
    Label(resumen_frame, text=f"Total ejemplos: {datos['total_ejemplos']}").pack(anchor="w")
    Label(resumen_frame, text=f"Total tags: {datos['total_tags']}").pack(anchor="w")
    
    # Palabras por nivel
    nivel_frame = Frame(parent_frame)
    nivel_frame.pack(anchor = "w", padx = 20, pady = 10)

    Label(nivel_frame, text = "Palabras por nivel").pack(anchor="w")

    for item in datos["palabras_por_nivel"]:
        texto = f"\t{item['nivel']}: {item['total']}"
        Label(nivel_frame, text = texto).pack(anchor="w")
    
    # Palabras por tipo
    tipo_frame = Frame(parent_frame)
    tipo_frame.pack(anchor = "w", padx = 20, pady = 10)

    Label(tipo_frame, text = "Palabras por tipo").pack(anchor="w")

    for item in datos["palabras_por_tipo"]:
        texto = f"\t{item['tipo']}: {item['total']}"
        Label(tipo_frame, text = texto).pack(anchor="w")
    
# botón para recargar estadísticas, lo ignoramos en el MVP
def refresh_dashboard():
    pass

if __name__ == "__main__":
    print(load_dashboard_data())
