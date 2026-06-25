from database import db

# Aquí tenemos las funciones encargadas de trabajar con el progreso de la base de datos. 

def obtener_progreso(vocabulario_id):
    progreso = db.fetch_one("SELECT * FROM vocabulario_progreso WHERE vocabulario_id = ?", [vocabulario_id])
    if progreso is None: 
        return None
    return dict(progreso)

def existe_progreso(vocabulario_id):
    fila = db.fetch_one("SELECT 1 FROM vocabulario_progreso WHERE vocabulario_id = ?",[vocabulario_id])
    return fila is not None # True si existe, False si no

def crear_progreso_inicial(vocabulario_id):
    db.execute_query("INSERT OR IGNORE INTO vocabulario_progreso(vocabulario_id, veces_vista, veces_repasada, aciertos, fallos, valoracion_ultima, peso_repaso, estado, primera_vez, ultima_vez) VALUES (?,0,0,0,0,NULL,1.0,'nueva',datetime('now'), datetime('now'))",[vocabulario_id])

def actualizar_progreso(progreso):
    db.execute_query("UPDATE vocabulario_progreso SET veces_vista = ?, veces_repasada = ?, aciertos = ?, fallos = ?, valoracion_ultima = ?, peso_repaso = ?, estado = ?, ultima_vez = datetime('now') WHERE vocabulario_id = ?",[progreso["veces_vista"],progreso["veces_repasada"],progreso["aciertos"],progreso["fallos"],progreso["valoracion_ultima"],progreso["peso_repaso"],progreso["estado"], progreso["vocabulario_id"]])

if __name__ == "__main__":
    vocabulario_id = "v_hallo"
    crear_progreso_inicial(vocabulario_id)
    print(existe_progreso("v_schrift"))
    pr = obtener_progreso("v_schrift")
    print(pr)
    pr["aciertos"] += 1
    actualizar_progreso(pr)
