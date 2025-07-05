"""
Importación de módulos locales que tienen funcionalidades específicas

"""
from clientes import clientes
from destinos import menu_destinos
from ventas import gestion_ventas
from estadisticas import estadisticas



def mostrar_menu():
    """
    Funcion que muestra el menú principal de opciones al usuario

    """
    print("\n 🛫  MENU PRINCIPAL  🛬 \n")
    print("1️⃣  CLIENTES")
    print("2️⃣  DESTINOS")
    print("3️⃣  VENTAS")
    print("4️⃣  ESTADISTICAS")
    print("5️⃣  SALIR\n")



bienvenida = True

# while True ==> Bucle principal del programa: se repite hasta que el usuario quiera salir

while True:

    if bienvenida == True:
        print("\n==============================================================\n")
        print("\n🫡    ¡BIENVENIDOS AL SISTEMA DE GESTION DE VIAJES!   🙌\n")
        print("🗺️   Explorá destinos, gestioná clientes, registrá ventas y analizá estadísticas..\n")

        # desactivo la bienvenida para que se vea 1 sola vez
        bienvenida = False

    mostrar_menu()  # Muestra el menú cada vez que comienza el bucle

    """
    try / except ==> Validación de entrada: Me aseguro con el except que el usuario ingrese un numero, sino le permite reintentar

    """
    try:
        opcion = int(input("Selecciona una opcion del Menu: "))

# Si el usuario ingresa algo que no es número, muestra un error y vuelve a pedir
    except ValueError:
        print("\n❌ Debes ingresar un numero del 1 al 5: ")
        continue
        

    """
match opcion ==> Llamado a los modulos segun la seleccion del usuario con un case por default que mostrara el mensaje de error si la opcion no existe

"""
    match opcion:
        case 1:
            print("\n👯 Entrando a Clientes...\n")
            clientes()

        case 2:
            print("\n✈️  Entrando a Destinos...\n")
            menu_destinos()

        case 3:
            print("\n💵  Entrando a Ventas...\n")
            gestion_ventas()

        case 4:
            print("\n📈  Entrando a Estadisticas...\n")
            estadisticas()

        case 5:

            confirmacion = input("\n🤔 Estas seguro que queres salir? S / N: ").upper()

            if confirmacion == "S":
                print("\n🫡  Hasta la proxima!!\n")
                break

            else:
                print("\n🔙  Volviendo al Menu...")
                
        case _:
            print("\n❌ Opcion no valida. Intenta nuevamente")




