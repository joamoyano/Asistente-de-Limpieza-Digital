import os
from organizador import organizar_archivos, EXTENSIONES_DEFAULT
from duplicados import buscar_duplicados, eliminar_duplicados
from grandes_antiguos import (
    buscar_archivos_grandes,
    buscar_archivos_antiguos,
    gestionar_archivos_detectados
)
from basura_espacio import limpiar_archivos_basura_y_vacios, analizar_uso_espacio
from utils import convertir_tamano, escribir_log
from datetime import datetime

EXCLUSIONES_PATH = "exclusiones.txt"

def cargar_exclusiones():
    if not os.path.exists(EXCLUSIONES_PATH):
        return []
    with open(EXCLUSIONES_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def ruta_excluida(ruta, exclusiones):
    return any(os.path.commonpath([ruta, excl]) == excl for excl in exclusiones)

def limpieza_total(ruta_base, palabra=None, fecha=None):
    exclusiones = cargar_exclusiones()
    log_lineas = []
    espacio_total_liberado = 0

    print("\n🔍 Buscando y eliminando duplicados...")
    duplicados = buscar_duplicados(ruta_base)
    if duplicados:
        for dup, _ in duplicados:
            try:
                if not ruta_excluida(dup, exclusiones):
                    espacio_total_liberado += os.path.getsize(dup)
                    os.remove(dup)
                    log_lineas.append(f"[DUPLICADO ELIMINADO] {dup}")
            except Exception as e:
                print(f"❌ Error al eliminar duplicado {dup}: {e}")
    else:
        print("✅ No se encontraron duplicados.")

    print("📦 Limpiando archivos grandes y antiguos...")
    grandes = buscar_archivos_grandes(ruta_base)
    antiguos = buscar_archivos_antiguos(ruta_base)

    total_detectados = grandes + antiguos
    total_detectados = [f for f in total_detectados if not ruta_excluida(f[0], exclusiones)]

    for ruta, size, _ in total_detectados:
        try:
            espacio_total_liberado += size
            os.remove(ruta)
            log_lineas.append(f"[GRANDE/ANTIGUO ELIMINADO] {ruta}")
        except Exception as e:
            print(f"❌ Error al eliminar archivo: {ruta}: {e}")

    print("🧼 Limpiando archivos basura y vacíos...")
    limpiar_archivos_basura_y_vacios(ruta_base)

    print("📊 Analizando uso de espacio restante...")
    analizar_uso_espacio(ruta_base)

    print("\n✅ Limpieza total completada.")
    print(f"💾 Espacio total recuperado: {convertir_tamano(espacio_total_liberado)}")

    log_lineas.append(f"[RESUMEN] Espacio recuperado: {convertir_tamano(espacio_total_liberado)}")
    escribir_log(log_lineas, titulo="Limpieza Total Automática")

