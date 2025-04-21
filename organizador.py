import os
import shutil
import json
from datetime import datetime
from utils import escribir_log

EXTENSIONES_DEFAULT = {
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Imágenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav"],
    "Comprimidos": [".zip", ".rar", ".7z"],
    "Ejecutables": [".exe", ".msi"],
    "Código": [".py", ".js", ".html", ".css"]
}

def cargar_categorias_personalizadas(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error al cargar categorías personalizadas: {e}")
        return EXTENSIONES_DEFAULT

def organizar_archivos(directorio, simular=False, verbose=True, palabra_clave=None, fecha_maxima=None, categorias=EXTENSIONES_DEFAULT):
    if not os.path.exists(directorio):
        print("📂 El directorio especificado no existe.")
        return

    cambios = []
    fecha_maxima_timestamp = None
    log_lineas = []

    if fecha_maxima:
        try:
            fecha_maxima_timestamp = datetime.strptime(fecha_maxima, "%Y-%m-%d").timestamp()
        except:
            print("⚠️ Fecha inválida. Usá el formato YYYY-MM-DD.")
            fecha_maxima_timestamp = None

    for carpeta_raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_raiz, archivo)

            if os.path.isfile(ruta_completa):
                _, extension = os.path.splitext(archivo)

                if palabra_clave and palabra_clave.lower() not in archivo.lower():
                    continue

                if fecha_maxima_timestamp:
                    fecha_archivo = os.path.getmtime(ruta_completa)
                    if fecha_archivo > fecha_maxima_timestamp:
                        continue

                for categoria, extensiones in categorias.items():
                    if extension.lower() in extensiones:
                        destino_carpeta = os.path.join(directorio, categoria)
                        destino_archivo = os.path.join(destino_carpeta, archivo)

                        if simular:
                            cambios.append((ruta_completa, destino_archivo))
                            log_lineas.append(f"[SIMULACIÓN] '{ruta_completa}' → '{destino_archivo}'")
                        else:
                            if not os.path.exists(destino_carpeta):
                                os.makedirs(destino_carpeta)
                            shutil.move(ruta_completa, destino_archivo)
                            if verbose:
                                print(f"🟢 Movido '{ruta_completa}' a '{destino_archivo}'")
                            log_lineas.append(f"[MOVIDO] '{ruta_completa}' → '{destino_archivo}'")
                        break

    if log_lineas:
        escribir_log(log_lineas, titulo="Organización de archivos")

    if simular:
        print("\n🔍 Modo simulación: estos archivos serían movidos:")
        for origen, destino in cambios:
            print(f"   - '{origen}' → '{destino}'")
        print("📝 Simulación registrada en el log.")
    elif verbose:
        print("✅ Organización completada. Acciones registradas en el log.")
