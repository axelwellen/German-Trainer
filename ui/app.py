# La responsabilidad es Crear la ventana principal y gestionar navegación.
# desde main tenemos que importar app y ejecutar app.run()
from tkinter import *
from ui import dashboard_view, vocab_view, flashcard_view

root = Tk()
nav_frame = Frame(root)
content_frame = Frame(root)
# monitor inferior
mensaje = StringVar()
# crea la ventana base:
# crear el root, poner títuo, tamaño y estructura principal
def crear_ventana_principal():
    root.title("German Trainer")
    root.resizable(True,True)
    crear_menu_navegacion() # creamos el menu de navegación antes del content_frame
    content_frame.pack(fill="both", expand = True)
    content_frame.config(width = 1000, height = 1000)
    content_frame.pack_propagate(False) # los hijos no pueden cambiar el tamaño
    mensaje.set("Bienvenido a German Trainer")
    monitor=Label(root, textvar=mensaje, justify="left", anchor ="w")
    monitor.pack(side="bottom", fill="x")
# crear el frame de navegación:
# poner botones o dejar espacio preparado para dashboard, vocabulario y salir
def crear_menu_navegacion():
    nav_frame.pack(side="top", fill="x")
    buttons_frame = Frame(nav_frame)
    buttons_frame.pack(anchor="center")
    # botón dashboard
    btn_dashboard = Button(buttons_frame, text="Dashboard", command = show_dashboard)
    btn_dashboard.config(width = 15, height = 2)
    btn_dashboard.pack(side="left", padx = 2, pady = 5)
    # botón vocabulario
    btn_vocabulario = Button(buttons_frame, text="Vocabulario", command = show_vocabulario)
    btn_vocabulario.config(width = 15, height = 2)
    btn_vocabulario.pack(side="left", padx = 1, pady = 5)
    # botón salir
    btn_salir = Button(buttons_frame, text="Salir", command = root.quit)
    btn_salir.config(width = 15, height =2)
    btn_salir.pack(side="left", padx = 1, pady = 5)
# limpia la zona central y muestra el dashboard
def show_dashboard():
    clear_content_frame()
    mensaje.set("Mostrando Dashboard")
    dashboard_view.render_dashboard(content_frame)
    # debe llamar a dashboard_view para que dibuje dentro del content_frame

# limpia la zona central y muestra la pantalla de vocabulario
def show_vocabulario():
    clear_content_frame()
    vocab_view.render_vocab_view(content_frame, show_flashcards)
    mensaje.set("Mostrar Vocabulario")

# limpia la zona central y muestra las tarjetas usando una lista de palabras
def show_flashcards(palabras):
    clear_content_frame()
    flashcard_view.render_flashcard_view(palabras, content_frame, show_vocabulario)
    mensaje.set("Mostrando Flashcards")

# borra lo que haya actualmente en la zona central
def clear_content_frame():
    mensaje.set("Limpiamos el Dashboard")
    for widget in content_frame.winfo_children():
        widget.destroy()

# prepara todo y arranca mainloop
def run():
    crear_ventana_principal()
    root.mainloop()

if __name__ == "__main__":
    run()


