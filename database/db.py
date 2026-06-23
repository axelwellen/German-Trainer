from models import config
import sqlite3

# La función de db.py es abrir y cerrar conexión con SQLite

# funciones

# devuelve una conexión a la base de datos
# debe usar la ruta guardada en config.py, se puede usar tambien directamente config.path
def get_connection():
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row # esto me permite hacer algo como un diccionario
    return connection
# usaremos with get_connection() as connection: 
# cursor = connection.cursor()
# python gestiona el cierre de conexión solo

# comprueba que la base de datos existe y que se puede abrir
# devuelve True/false o un mensaje tipo "conexión correcta"
def test_connection():
    try:
        conexion = get_connection()
        conexion.close()
        return "Conexión correcta."
    except Exception as e:
        print(f"Error:{type(e).__name__}")

# para centralizar consultas que modifiquen la base de datos
def execute_query(query, params=None):
    pass

# permite hacer una query que devuelva un resultado
def fetch_one(query, params=None):
    with get_connection() as connection:
        cursor = connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        return cursor.fetchone()

# permite hacer una query que devuelva varios resultados
def fetch_all(query, params=None):
    with get_connection() as connection:
        cursor = connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        return cursor.fetchall()

# Si ejecutamos esto como clase principal se ejecutará:
if __name__ == "__main__":
    print(test_connection())
