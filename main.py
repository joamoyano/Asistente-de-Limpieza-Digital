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

def mostrar_menu():
    print(Fore.CYAN + "=" * 50)
    print(Style.BRIGHT + Fore.CYAN + " Menú principal ".center(50, "="))
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "[1] Simular organización de archivos")
    print(Fore.CYAN + "[2] Organizar archivos (modo real)")
    print(Fore.CYAN + "[3] Ver registro de acciones")
    print(Fore.CYAN + "[4] Limpiar registro")
    print(Fore.CYAN + "[5] Buscar archivos duplicados")
    print(Fore.CYAN + "[6] Buscar archivos grandes o antiguos")
    print(Fore.CYAN + "[7] Salir")
    print(Fore.CYAN + "=" * 50)

def main():
    while True:
        limpiar_pantalla()
        mostrar_logo()
        mostrar_menu()
        opcion = input(Fore.GREEN + "Selecciona una opción: ")

        if opcion in ["1", "2"]:
            ruta = input(Fore.YELLOW + "\n📁 Ruta de la carpeta a organizar: ").strip()
            verbose = input("🔍 ¿Mostrar detalles? (s/n): ").lower() == "s"
            simular = opcion == "1"
            palabra = input("📝 ¿Filtrar por palabra clave en el nombre? (Enter para omitir): ").strip() or None
            fecha = input("📅 ¿Filtrar archivos modificados antes de qué fecha? (YYYY-MM-DD o Enter para omitir): ").strip() or None
            usar_json = input("📑 ¿Usar archivo JSON de categorías personalizadas? (s/n): ").lower()
            categorias = cargar_categorias_personalizadas("categorias_personalizadas.json") if usar_json == "s" else EXTENSIONES_DEFAULT
            organizar_archivos(ruta, simular, verbose, palabra, fecha, categorias)

        elif opcion == "3":
            limpiar_pantalla()
            mostrar_logo()
            mostrar_log()
            input(Fore.YELLOW + "\nPresioná Enter para volver al menú...")

        elif opcion == "4":
            confirmar = input(Fore.RED + "⚠️ ¿Seguro que querés borrar el log? (s/n): ").lower()
            if confirmar == "s":
                limpiar_log()
            else:
                print("❌ Operación cancelada.")
            input("\nPresioná Enter para continuar...")

        elif opcion == "5":
            ruta = input(Fore.YELLOW + "\n📁 Ruta a escanear para duplicados: ").strip()
            limpiar_pantalla()
            mostrar_logo()
            print(Fore.CYAN + "🔍 Buscando archivos duplicados...\n")
            duplicados = buscar_duplicados(ruta)
            if duplicados:
                espacio_total = sum(os.path.getsize(d[0]) for d in duplicados if os.path.exists(d[0]))
                print(Fore.RED + Style.BRIGHT + f"⚠️ Se encontraron {len(duplicados)} archivos duplicados.")
                print(Fore.LIGHTBLUE_EX + f"💾 Espacio potencialmente recuperable: {convertir_tamano(espacio_total)}\n")
                for dup, original in duplicados:
                    print(Fore.LIGHTRED_EX + f"📁 Duplicado: {dup}\n↪️ Original: {original}\n")
                print(Fore.CYAN + "\n¿Qué querés hacer con los duplicados?")
                print("[1] No hacer nada (solo ver)")
                print("[2] Mover a carpeta 'Duplicados'")
                print("[3] Eliminar duplicados")
                accion = input(Fore.GREEN + "Elegí una opción: ").strip()
                if accion == "2":
                    mover_duplicados(duplicados, ruta)
                elif accion == "3":
                    confirmar = input(Fore.RED + "⚠️ ¿Seguro que querés eliminar los duplicados? (s/n): ").lower()
                    if confirmar == "s":
                        eliminar_duplicados(duplicados)
            else:
                print(Fore.GREEN + "✅ No se encontraron duplicados.")
            input(Fore.YELLOW + "\nPresioná Enter para volver al menú...")

        elif opcion == "6":
            ruta = input(Fore.YELLOW + "\n📁 Ruta de la carpeta a analizar: ").strip()
            print(Fore.CYAN + "\n¿Querés buscar archivos grandes o antiguos?")
            print("[1] Archivos grandes")
            print("[2] Archivos antiguos")
            eleccion = input(Fore.GREEN + "Selecciona una opción: ").strip()

            if eleccion == "1":
                valor_mb = input("📏 Tamaño mínimo en MB (por defecto 100): ").strip()
                minimo_bytes = int(valor_mb) * 1024 * 1024 if valor_mb.isdigit() else 100 * 1024 * 1024
                resultado = buscar_archivos_grandes(ruta, minimo_bytes)
                mostrar_lista_archivos(resultado, titulo=f"Archivos mayores a {convertir_tamano(minimo_bytes)}")

            elif eleccion == "2":
                dias = input("📆 Días sin modificación (por defecto 180): ").strip()
                dias = int(dias) if dias.isdigit() else 180
                resultado = buscar_archivos_antiguos(ruta, dias)
                mostrar_lista_archivos(resultado, titulo=f"Archivos sin modificar hace más de {dias} días")
            else:
                print(Fore.RED + "⚠️ Opción inválida.")
                input("\nPresioná Enter para volver al menú...")
                continue

            if resultado:
                print(Fore.CYAN + "\n¿Qué querés hacer con estos archivos?")
                print("[1] No hacer nada")
                print("[2] Mover a carpeta 'Archivos_Limpieza'")
                print("[3] Eliminar archivos")
                print("[4] Exportar a CSV")

                accion = input(Fore.GREEN + "Seleccioná una acción: ").strip()

                if accion == "2":
                    gestionar_archivos_detectados(resultado, "mover", ruta)
                elif accion == "3":
                    gestionar_archivos_detectados(resultado, "eliminar", ruta)
                elif accion == "4":
                    gestionar_archivos_detectados(resultado, "exportar", ruta)
                else:
                    print("🟡 No se realizó ninguna acción.")

            input(Fore.YELLOW + "\nPresioná Enter para volver al menú...")


        elif opcion == "7":
            print(Fore.MAGENTA + "\n👋 Saliendo del asistente. ¡Hasta la próxima!\n")
            break

        else:
            print(Fore.RED + "⚠️ Opción inválida.")
            input("\nPresioná Enter para continuar...")

if __name__ == "__main__":
    main()
