# Script para crear las tablas de progreso del vocabulario y los resultados de ejercicios
from database import db 

def crear_tabla_vocabulario_progreso():
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS vocabulario_progreso (
            vocabulario_id TEXT PRIMARY KEY,
            veces_vista INTEGER DEFAULT 0,
            veces_repasada INTEGER DEFAULT 0,
            aciertos INTEGER DEFAULT 0,
            fallos INTEGER DEFAULT 0,
            valoracion_ultima INTEGER,
            peso_repaso REAL DEFAULT 1.0,
            estado TEXT DEFAULT 'nueva',
            primera_vez TEXT,
            ultima_vez TEXT,
            FOREIGN KEY (vocabulario_id) REFERENCES vocabulario(id)
        );
    """)

def crear_tabla_ejercicio_resultados():
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS ejercicio_resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vocabulario_id TEXT NOT NULL,
            tipo_ejercicio TEXT NOT NULL,
            respuesta_usuario TEXT,
            respuesta_correcta TEXT,
            es_correcta INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (vocabulario_id) REFERENCES vocabulario(id)
        );
    """)

# Al ejecutarlo, se crean las tablas sin romper nada
def ejecutar_migracion():
    crear_tabla_vocabulario_progreso()
    crear_tabla_ejercicio_resultados()
    print("Migración v0.2 completada correctamente.")

if __name__ == "__main__":
    ejecutar_migracion()

