import os
import csv
import shutil
from datetime import datetime, timedelta
from utils import convertir_tamano, timestamp_a_fecha, escribir_log

def buscar_archivos_grandes(directorio, minimo_bytes=100 * 1024 * 1024):
    archivos_grandes = []
    for carpeta_raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            ruta = os.path.join(carpeta_raiz, archivo)
            if os.path.isfile(ruta):
                size = os.path.getsize(ruta)
                if size >= minimo_bytes:
                    archivos_grandes.append((ruta, size, os.path.getmtime(ruta)))
    archivos_grandes.sort(key=lambda x: x[1], reverse=True)
    return archivos_grandes

def buscar_archivos_antiguos(directorio, dias=180):
    archivos_antiguos = []
    fecha_limite = datetime.now() - timedelta(days=dias)
    for carpeta_raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            ruta = os.path.join(carpeta_raiz, archivo)
            if os.path.isfile(ruta):
                mod_time = os.path.getmtime(ruta)
                if datetime.fromtimestamp(mod_time) <= fecha_limite:
                    size = os.path.getsize(ruta)
                    archivos_antiguos.append((ruta, size, mod_time))
    archivos_antiguos.sort(key=lambda x: x[2])
    return archivos_antiguos

def mostrar_lista_archivos(lista, titulo=""):
    if not lista:
        print("✅ No se encontraron archivos.")
        return
    print(f"\n📋 {titulo} ({len(lista)} archivos):\n")
    for ruta, size, mod_time in lista:
        print(f"📁 {ruta}")
        print(f"   - Tamaño: {convertir_tamano(size)}")
        print(f"   - Última modificación: {timestamp_a_fecha(mod_time)}\n")

def gestionar_archivos_detectados(lista, accion, ruta_base=None):
    if not lista:
        print("❌ No hay archivos para gestionar.")
        return

    log_lineas = []
    espacio_total = 0

    if accion == "mover":
        destino = os.path.join(ruta_base, "Archivos_Limpieza")
        os.makedirs(destino, exist_ok=True)
        for ruta, size, _ in lista:
            try:
                nombre = os.path.basename(ruta)
                destino_final = os.path.join(destino, nombre)
                contador = 1
                while os.path.exists(destino_final):
                    base, ext = os.path.splitext(nombre)
                    destino_final = os.path.join(destino, f"{base}_{contador}{ext}")
                    contador += 1
                shutil.move(ruta, destino_final)
                espacio_total += size
                log_lineas.append(f"[MOVIDO] '{ruta}' → '{destino_final}'")
            except Exception as e:
                print(f"❌ Error al mover {ruta}: {e}")
        print(f"📦 Archivos movidos a {destino}")
        log_lineas.append(f"💾 Espacio movido: {convertir_tamano(espacio_total)}")
        escribir_log(log_lineas, titulo="Movimiento de archivos grandes/antiguos")

    elif accion == "eliminar":
        confirmar = input("⚠️ ¿Seguro que querés eliminar estos archivos? (s/n): ").lower()
        if confirmar != "s":
            print("❌ Operación cancelada.")
            return
        for ruta, size, _ in lista:
            try:
                os.remove(ruta)
                espacio_total += size
                log_lineas.append(f"[ELIMINADO] '{ruta}'")
            except Exception as e:
                print(f"❌ Error al eliminar {ruta}: {e}")
        print(f"🗑️ Archivos eliminados.")
        log_lineas.append(f"💾 Espacio liberado: {convertir_tamano(espacio_total)}")
        escribir_log(log_lineas, titulo="Eliminación de archivos grandes/antiguos")

    elif accion == "exportar":
        nombre_csv = os.path.join(ruta_base, "reporte_archivos_detectados.csv")
        with open(nombre_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Ruta", "Tamaño", "Última Modificación"])
            for ruta, size, mod_time in lista:
                writer.writerow([ruta, convertir_tamano(size), timestamp_a_fecha(mod_time)])
        print(f"📤 Exportado a: {nombre_csv}")
