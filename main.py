import os
from organizador import (
    organizar_archivos,
    cargar_categorias_personalizadas,
    EXTENSIONES_DEFAULT
)
from utils import mostrar_log, limpiar_log
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_logo():
    print(Fore.YELLOW + Style.BRIGHT + """
   ___        __          _           _      
  / _ \ ___  / _| ___  __| | ___ _ __(_) ___ 
 | | | / _ \| |_ / _ \/ _` |/ _ \ '__| |/ __|
 | |_| | (_) |  _|  __/ (_| |  __/ |  | | (__ 
  \___/ \___/|_|  \___|\__,_|\___|_|  |_|\___|
        🧹 Asistente de Limpieza Digital
    """)

def mostrar_menu():
    print(Fore.CYAN + "=" * 50)
    print(Style.BRIGHT + Fore.CYAN + " Menú principal ".center(50, "="))
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "[1] Simular organización de archivos")
    print(Fore.CYAN + "[2] Organizar archivos (modo real)")
    print(Fore.CYAN + "[3] Ver registro de acciones")
    print(Fore.CYAN + "[4] Limpiar registro")
    print(Fore.CYAN + "[5] Salir")
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

            palabra = input("📝 ¿Filtrar por palabra clave en el nombre? (Enter para omitir): ").strip()
            palabra = palabra if palabra else None

            fecha = input("📅 ¿Filtrar archivos modificados antes de qué fecha? (YYYY-MM-DD o Enter para omitir): ").strip()
            fecha = fecha if fecha else None

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
            print(Fore.MAGENTA + "\n👋 Saliendo del asistente. ¡Hasta la próxima!\n")
            break
        else:
            print(Fore.RED + "⚠️ Opción inválida.")
            input("\nPresioná Enter para continuar...")

if __name__ == "__main__":
    main()
