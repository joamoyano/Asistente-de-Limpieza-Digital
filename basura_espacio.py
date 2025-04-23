import os
import shutil
from collections import defaultdict
from utils import convertir_tamano, escribir_log

EXTENSIONES_BASURA = ['.tmp', '.log', '.bak', '.ds_store', 'thumbs.db']

def limpiar_archivos_basura_y_vacios(ruta_base):
    archivos_eliminados = []
    carpetas_vacias = []

    for carpeta_raiz, carpetas, archivos in os.walk(ruta_base, topdown=False):
        # Archivos basura o vacíos
        for archivo in archivos:
            ruta = os.path.join(carpeta_raiz, archivo)
            ext = os.path.splitext(archivo)[1].lower()
            try:
                if ext in EXTENSIONES_BASURA or os.path.getsize(ruta) == 0:
                    os.remove(ruta)
                    archivos_eliminados.append(ruta)
            except Exception as e:
                print(f"❌ No se pudo eliminar {ruta}: {e}")

        # Carpetas vacías
        if not os.listdir(carpeta_raiz):
            try:
                os.rmdir(carpeta_raiz)
                carpetas_vacias.append(carpeta_raiz)
            except Exception as e:
                print(f"❌ No se pudo eliminar carpeta vacía {carpeta_raiz}: {e}")

    print(f"🗑️ Se eliminaron {len(archivos_eliminados)} archivos basura o vacíos.")
    print(f"📁 Se eliminaron {len(carpetas_vacias)} carpetas vacías.")

    log_lineas = [f"[ELIMINADO] {ruta}" for ruta in archivos_eliminados + carpetas_vacias]
    escribir_log(log_lineas, titulo="Limpieza de archivos basura y vacíos")

def analizar_uso_espacio(ruta_base):
    categorias = {
        "Imágenes": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        "Videos": ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
        "Documentos": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
        "Audio": ['.mp3', '.wav', '.aac', '.flac'],
        "Comprimidos": ['.zip', '.rar', '.7z', '.tar', '.gz']
    }

    totales_tamano = defaultdict(int)
    totales_archivos = defaultdict(int)
    otros_tamano = 0
    otros_archivos = 0

    for carpeta_raiz, _, archivos in os.walk(ruta_base):
        for archivo in archivos:
            ruta = os.path.join(carpeta_raiz, archivo)
            try:
                ext = os.path.splitext(archivo)[1].lower()
                size = os.path.getsize(ruta)
                encontrada = False

                for categoria, extensiones in categorias.items():
                    if ext in extensiones:
                        totales_tamano[categoria] += size
                        totales_archivos[categoria] += 1
                        encontrada = True
                        break

                if not encontrada:
                    otros_tamano += size
                    otros_archivos += 1
            except Exception as e:
                print(f"❌ No se pudo leer {ruta}: {e}")

    print("\n📊 Uso de espacio por tipo de archivo:\n")

    for categoria in categorias:
        total = totales_tamano[categoria]
        cantidad = totales_archivos[categoria]
        print(f"📂 {categoria}")
        print(f"   - Tamaño total: {convertir_tamano(total)}")
        print(f"   - Archivos: {cantidad}\n")

    print("📂 Otros")
    print(f"   - Tamaño total: {convertir_tamano(otros_tamano)}")
    print(f"   - Archivos: {otros_archivos}\n")
