import os
from datetime import datetime

def convertir_tamano(bytes):
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unidad}"
        bytes /= 1024

def timestamp_a_fecha(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def generar_encabezado_log(titulo="Registro"):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"\n{'=' * 50}\n📅 {titulo} - {ahora}\n"

def escribir_log(lineas, archivo="registro_organizacion.txt", titulo="Registro"):
    with open(archivo, "a", encoding="utf-8") as log:
        log.write(generar_encabezado_log(titulo))
        for linea in lineas:
            log.write(linea + "\n")
        log.write("=" * 50 + "\n")

def mostrar_log(archivo="registro_organizacion.txt"):
    if not os.path.exists(archivo):
        print("📭 El log aún no existe.")
        return
    print("\n📖 Contenido del log:\n")
    with open(archivo, "r", encoding="utf-8") as log:
        print(log.read())

def limpiar_log(archivo="registro_organizacion.txt"):
    if os.path.exists(archivo):
        with open(archivo, "w", encoding="utf-8") as log:
            log.write("")
        print("🧼 Log limpiado correctamente.")
    else:
        print("📭 El log aún no existe.")
