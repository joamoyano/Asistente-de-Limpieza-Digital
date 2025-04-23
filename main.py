import os
from organizador import (
    organizar_archivos,
    cargar_categorias_personalizadas,
    EXTENSIONES_DEFAULT
)
from grandes_antiguos import (
    buscar_archivos_grandes,
    buscar_archivos_antiguos,
    mostrar_lista_archivos,
    gestionar_archivos_detectados
)
from limpieza_total import limpieza_total
from basura_espacio import limpiar_archivos_basura_y_vacios, analizar_uso_espacio
from utils import mostrar_log, limpiar_log, convertir_tamano
from duplicados import buscar_duplicados, mover_duplicados, eliminar_duplicados
from colorama import Fore, Style, init

init(autoreset=True)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_logo():
    print(Fore.GREEN + Style.BRIGHT + """
                                                             
 █████╗ ███████╗██╗███████╗████████╗███████╗███╗   ██╗████████╗███████╗    ██████╗ ███████╗                  
██╔══██╗██╔════╝██║██╔════╝╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝    ██╔══██╗██╔════╝                  
███████║███████╗██║███████╗   ██║   █████╗  ██╔██╗ ██║   ██║   █████╗      ██║  ██║█████╗                    
██╔══██║╚════██║██║╚════██║   ██║   ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝      ██║  ██║██╔══╝                    
██║  ██║███████║██║███████║   ██║   ███████╗██║ ╚████║   ██║   ███████╗    ██████╔╝███████╗                  
╚═╝  ╚═╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝    ╚═════╝ ╚══════╝                  
                                                                                                             
██╗     ██╗███╗   ███╗██████╗ ██╗███████╗███████╗ █████╗     ██████╗ ██╗ ██████╗ ██╗████████╗ █████╗ ██╗     
██║     ██║████╗ ████║██╔══██╗██║██╔════╝╚══███╔╝██╔══██╗    ██╔══██╗██║██╔════╝ ██║╚══██╔══╝██╔══██╗██║     
██║     ██║██╔████╔██║██████╔╝██║█████╗    ███╔╝ ███████║    ██║  ██║██║██║  ███╗██║   ██║   ███████║██║     
██║     ██║██║╚██╔╝██║██╔═══╝ ██║██╔══╝   ███╔╝  ██╔══██║    ██║  ██║██║██║   ██║██║   ██║   ██╔══██║██║     
███████╗██║██║ ╚═╝ ██║██║     ██║███████╗███████╗██║  ██║    ██████╔╝██║╚██████╔╝██║   ██║   ██║  ██║███████╗
╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
    """)

def menu_principal():
    print(Fore.CYAN + "=" * 50)
    print(Style.BRIGHT + Fore.CYAN + " Menú principal ".center(50, "="))
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "[1] Organización de archivos")
    print(Fore.CYAN + "[2] Búsqueda y limpieza avanzada")
    print(Fore.CYAN + "[3] Ver/limpiar registro")
    print(Fore.CYAN + "[4] Limpieza Total automática")
    print(Fore.CYAN + "[5] Salir")
    print(Fore.CYAN + "=" * 50)

def submenu_organizacion():
    while True:
        limpiar_pantalla()
        mostrar_logo()
        print(Fore.CYAN + "=" * 50)
        print(Style.BRIGHT + Fore.CYAN + " Organización de archivos ".center(50, "="))
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + "[1] Simular organización")
        print(Fore.CYAN + "[2] Organización real")
        print(Fore.CYAN + "[3] Volver al menú principal")
        opcion = input(Fore.GREEN + "Selecciona una opción: ").strip()

        if opcion in ["1", "2"]:
            ruta = input("📁 Ruta: ").strip()
            verbose = input("🔍 Mostrar detalles (s/n): ").lower() == "s"
            simular = opcion == "1"
            palabra = input("📝 Palabra clave (Enter para omitir): ").strip() or None
            fecha = input("📅 Filtrar por fecha (YYYY-MM-DD o Enter): ").strip() or None
            usar_json = input("📑 Usar JSON personalizado (s/n): ").lower()
            categorias = cargar_categorias_personalizadas("categorias_personalizadas.json") if usar_json == "s" else EXTENSIONES_DEFAULT
            organizar_archivos(ruta, simular, verbose, palabra, fecha, categorias)

            volver = input(Fore.YELLOW + "\n¿Volver al menú de organización? (s/n): ").strip().lower()
            if volver != "s":
                break

        elif opcion == "3":
            break

        else:
            print(Fore.RED + "⚠️ Opción inválida.")
            input(Fore.YELLOW + "\nPresioná Enter para continuar...")


def submenu_limpieza_avanzada():
    while True:
        limpiar_pantalla()
        mostrar_logo()
        print(Fore.CYAN + "=" * 50)
        print(Style.BRIGHT + Fore.CYAN + " Búsqueda y limpieza avanzada ".center(50, "="))
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + "[1] Buscar archivos duplicados")
        print(Fore.CYAN + "[2] Archivos grandes o antiguos")
        print(Fore.CYAN + "[3] Limpieza basura y análisis de espacio")
        print(Fore.CYAN + "[4] Volver al menú principal")
        opcion = input(Fore.GREEN + "Selecciona una opción: ").strip()

        if opcion == "1":
            ruta = input("📁 Ruta: ").strip()
            duplicados = buscar_duplicados(ruta)
            if duplicados:
                espacio_total = sum(os.path.getsize(d[0]) for d in duplicados if os.path.exists(d[0]))
                print(Fore.RED + f"⚠️ {len(duplicados)} duplicados encontrados.")
                print(Fore.LIGHTBLUE_EX + f"💾 Espacio recuperable: {convertir_tamano(espacio_total)}\n")
                for dup, orig in duplicados:
                    print(f"📁 {dup}\n↪️ {orig}\n")
                print("[1] No hacer nada | [2] Mover | [3] Eliminar")
                acc = input("Opción: ").strip()
                if acc == "2":
                    mover_duplicados(duplicados, ruta)
                elif acc == "3":
                    if input("¿Seguro que querés eliminar? (s/n): ").lower() == "s":
                        eliminar_duplicados(duplicados)
            else:
                print("✅ No se encontraron duplicados.")

        elif opcion == "2":
            ruta = input("📁 Ruta: ").strip()
            print("[1] Grandes | [2] Antiguos")
            tipo = input("Opción: ").strip()
            if tipo == "1":
                val = input("Tamaño mínimo en MB (default 100): ").strip()
                min_bytes = int(val) * 1024 * 1024 if val.isdigit() else 100 * 1024 * 1024
                resultado = buscar_archivos_grandes(ruta, min_bytes)
                mostrar_lista_archivos(resultado, f"Archivos > {convertir_tamano(min_bytes)}")
            else:
                dias = input("Días sin modificar (default 180): ").strip()
                dias = int(dias) if dias.isdigit() else 180
                resultado = buscar_archivos_antiguos(ruta, dias)
                mostrar_lista_archivos(resultado, f"No modificados en {dias} días")

            if resultado:
                print("[1] Nada | [2] Mover | [3] Eliminar | [4] Exportar CSV")
                acc = input("Opción: ").strip()
                if acc in ["2", "3", "4"]:
                    acciones = {"2": "mover", "3": "eliminar", "4": "exportar"}
                    gestionar_archivos_detectados(resultado, acciones[acc], ruta)

        elif opcion == "3":
            ruta = input("📁 Ruta: ").strip()
            print("[1] Limpiar basura | [2] Analizar uso | [3] Ambas")
            acc = input("Opción: ").strip()
            if acc in ["1", "3"]:
                limpiar_archivos_basura_y_vacios(ruta)
            if acc in ["2", "3"]:
                analizar_uso_espacio(ruta)

        elif opcion == "4":
            break

        else:
            print(Fore.RED + "⚠️ Opción inválida.")

        volver = input(Fore.YELLOW + "\n¿Volver al menú de limpieza avanzada? (s/n): ").strip().lower()
        if volver != "s":
            break

def submenu_registro():
    while True:
        limpiar_pantalla()
        mostrar_logo()
        print(Fore.CYAN + "=" * 50)
        print(Style.BRIGHT + Fore.CYAN + " Registro de acciones ".center(50, "="))
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + "[1] Ver registro")
        print(Fore.CYAN + "[2] Limpiar registro")
        print(Fore.CYAN + "[3] Volver al menú principal")
        print(Fore.CYAN + "=" * 50)

        opcion = input(Fore.GREEN + "Seleccioná una opción: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            mostrar_logo()
            mostrar_log()

        elif opcion == "2":
            confirmar = input(Fore.RED + "⚠️ ¿Seguro que querés borrar el log? (s/n): ").lower()
            if confirmar == "s":
                limpiar_log()
                print(Fore.GREEN + "✅ Registro limpiado correctamente.")
            else:
                print(Fore.LIGHTBLACK_EX + "❌ Operación cancelada.")

        elif opcion == "3":
            break

        else:
            print(Fore.RED + "⚠️ Opción inválida.")

        volver = input(Fore.YELLOW + "\n¿Volver al menú de registro? (s/n): ").strip().lower()
        if volver != "s":
            break


def main():
    while True:
        limpiar_pantalla()
        mostrar_logo()
        menu_principal()
        opcion = input(Fore.GREEN + "Seleccioná una opción: ").strip()

        if opcion == "1":
            submenu_organizacion()

        elif opcion == "2":
            submenu_limpieza_avanzada()

        elif opcion == "3":
            submenu_registro()

        elif opcion == "4":
            limpiar_pantalla()
            mostrar_logo()
            print(Fore.CYAN + "=" * 50)
            print(Style.BRIGHT + Fore.CYAN + " Limpieza Total automática ".center(50, "="))
            print(Fore.CYAN + "=" * 50)
            ruta = input(Fore.YELLOW + "\n📁 Ruta de la carpeta para limpieza total: ").strip()
            palabra = input("📝 ¿Filtrar por palabra clave? (Enter para omitir): ").strip() or None
            fecha = input("📅 ¿Filtrar archivos modificados antes de qué fecha? (YYYY-MM-DD o Enter): ").strip() or None

            print(Fore.CYAN + "\n⚙️ Ejecutando limpieza total...\n")
            limpieza_total(ruta, palabra, fecha)
            input(Fore.YELLOW + "\nPresioná Enter para volver al menú...")

        elif opcion == "5":
            print(Fore.MAGENTA + "\n👋 ¡Hasta la próxima!\n")
            break

        else:
            print(Fore.RED + "⚠️ Opción inválida.")
            input("Presioná Enter para continuar...")

if __name__ == "__main__":
    main()
