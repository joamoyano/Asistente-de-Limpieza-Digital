import os
import hashlib
import shutil
from utils import escribir_log

def calcular_hash(archivo, bloque=65536):
    hasher = hashlib.md5()
    try:
        with open(archivo, 'rb') as f:
            buf = f.read(bloque)
            while buf:
                hasher.update(buf)
                buf = f.read(bloque)
        return hasher.hexdigest()
    except:
        return None

def buscar_duplicados(directorio):
    hashes = {}
    duplicados = []

    for carpeta_raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_raiz, archivo)

            if os.path.isfile(ruta_completa):
                hash_archivo = calcular_hash(ruta_completa)
                if not hash_archivo:
                    continue

                if hash_archivo in hashes:
                    duplicados.append((ruta_completa, hashes[hash_archivo]))
                else:
                    hashes[hash_archivo] = ruta_completa

    return duplicados

def eliminar_duplicados(lista_duplicados):
    log_lineas = []
    for duplicado, original in lista_duplicados:
        try:
            os.remove(duplicado)
            print(f"🗑️ Eliminado: {duplicado}")
            log_lineas.append(f"[ELIMINADO] '{duplicado}' (duplicado de '{original}')")
        except Exception as e:
            print(f"❌ Error al eliminar {duplicado}: {e}")
    if log_lineas:
        escribir_log(log_lineas, titulo="Eliminación de duplicados")

def mover_duplicados(lista_duplicados, destino_base):
    destino = os.path.join(destino_base, "Duplicados")
    os.makedirs(destino, exist_ok=True)

    log_lineas = []

    for duplicado, original in lista_duplicados:
        try:
            nombre = os.path.basename(duplicado)
            destino_final = os.path.join(destino, nombre)

            contador = 1
            while os.path.exists(destino_final):
                nombre_base, ext = os.path.splitext(nombre)
                destino_final = os.path.join(destino, f"{nombre_base}_{contador}{ext}")
                contador += 1

            shutil.move(duplicado, destino_final)
            print(f"📦 Movido: {duplicado} → {destino_final}")
            log_lineas.append(f"[MOVIDO] '{duplicado}' → '{destino_final}' (duplicado de '{original}')")
        except Exception as e:
            print(f"❌ Error al mover {duplicado}: {e}")

    if log_lineas:
        escribir_log(log_lineas, titulo="Movimiento de duplicados")
