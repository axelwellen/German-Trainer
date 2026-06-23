from models import config
import shutil
import datetime
from pathlib import Path
# Este script copia el .db actual con fecha y hora
# ejemplo de nombre: vocabulario_backup_2026_06_20_1530.db
# config.DB_PATH es donde está la base de datos (tiene nombre=
# config.DB_BACKUP_PATH es donde se tiene que guardar la copia (no tiene nombre)


def crear_backup_db():
    carpeta_destino = Path(config.DB_BACKUP_PATH)
    origen = Path(config.DB_PATH)
    nombre_backup = generar_nombre_backup()
    # se podría mirar si existe la carpeta de destino con carpeta_destino.mkdir(parents = True, exist_ok = True)
    destino = carpeta_destino / nombre_backup # forma de hacerlo con path
    shutil.copy2(origen,destino)
    
    print("Se ha creado una copia de la base de datos llamada: " + nombre_backup + " en la ruta: " + str(carpeta_destino))

def generar_nombre_backup():
    origen = Path(config.DB_PATH)
    dt = datetime.datetime.now()
    new_name = origen.stem + f"_backup_{dt.year}_{dt.month:02d}_{dt.day:02d}_{dt.hour:02d}{dt.minute:02d}" + origen.suffix
    return new_name

if __name__ == "__main__":
    crear_backup_db()
