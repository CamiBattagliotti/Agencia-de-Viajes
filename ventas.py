
import json
import os
from clientes import cargar_datos as leer_clientes
from tabulate import tabulate
from datetime import datetime
import requests  # ==> Importo la biblioteca requests para poder hacer solicitudes HTTP a APIs externas
import csv


"""
Rutas a los archivos json:

"""
json_clientes = "Archivos-Json/clientes.json"
json_destinos = "Archivos-Json/destinos.json"
json_ventas = "Archivos-Json/ventas.json"


"""
Funciones responsables de obtener los datos desde los archivos JSON existentes:

"""

def leer_destinos():
    """
    Lee los datos de destinos turísticos desde el archivo JSON.
    Devuelve una lista de diccionarios con los destinos disponibles.
    """

    if not os.path.exists(json_destinos):
        return []
    with open(json_destinos, "r", encoding='utf-8') as destinos:
        return json.load(destinos)

def leer_ventas():
    """
    Lee los datos de ventas realizadas desde el archivo JSON.
    Devuelve una lista de diccionarios con las ventas registradas.
    """
    if not os.path.exists(json_ventas):
        return[]
    with open(json_ventas, 'r', encoding='utf-8') as ventas:
        return json.load(ventas)
    
"""
Funciones para guardar en los archivos json las modificaciones realizadas:

"""
    
def guardar_ventas(ventas):
    """
    Guarda las ventas en el archivo json de ventas
    """
    with open(json_ventas, 'w', encoding='utf-8') as v:
        json.dump(ventas, v, indent=2, ensure_ascii=False)
    

def guardar_destinos(destinos):
    """
    Guarda los destinos en el archivo json de destinos
    """
    with open(json_destinos, 'w', encoding='utf-8') as d:
        json.dump(destinos, d, indent=2, ensure_ascii=False)
    

"""
Leo los datos guardados en los archivos json y los almaceno en variables para trabajar con ellos en el programa

"""
clientes = leer_clientes()
destinos = leer_destinos()
ventas = leer_ventas()


"""
Funciones auxiliares:

"""

def borrar():
    """
    Limpia la consola para mantener una interfaz más clara.
    """
    os.system('cls' if os.name == 'nt' else 'clear')



def buscar_cliente_DNI():
    """
    Solicita al usuario un DNI y busca el cliente correspondiente.
    Devuelve un diccionario con los datos del cliente si se encuentra, None si no.
    """
    dni = input("\nIngrese el DNI del cliente: ")

    for c in clientes:
        if c['dni'] == dni:
            print(f"\n✅ El cliente seleccionado es: {c['nombre'].title()} {c['apellido'].title()}\n")
            return c
    
    print("\n❌ Cliente no encontrado \n")

    return None



def mostrar_destinos():
    """
    Muestra en formato de tabla todos los destinos turísticos disponibles.
    """
    tabla = []
    for d in destinos:
        fila = [d['id'], d['nombre'], f"$ {d['precio']}", d['disponibilidad']]
        tabla.append(fila)

    headers = ["Id", "Nombre", "Precio", "Disponiblidad"]

    print(tabulate(tabla, headers, tablefmt="fancy_grid"))



def buscar_destino_ID():
    """
    Solicita un ID de destino al usuario y busca si existe.
    Devuelve un diccionario del destino si se encuentra o None en caso contrario.
    """
    try:
        id = int(input("\nIngrese el ID del destino: "))
    except ValueError:
        print("\n❌ Error. Debe ingresar un numero entero\n")
        return None

    for d in destinos:
        if d['id'] == id:
            print(f"\n🏝️   El destino seleccionado es: {d['nombre']}")
            return d
    
    print("\n❌ Destino no encontrado\n")
    return None



def seleccionar_destino():
    """
    Despliega los destinos y permite seleccionar uno por su ID.
    Devuelve un diccionario del destino seleccionado, o None si no se elige ninguno válido.
    """
    print("🏝️   Los destinos disponibles son: \n")
    mostrar_destinos()

    destino = buscar_destino_ID()
    return destino


def solicitar_cantidad(destino):
    """
    Pide al usuario la cantidad de reservas para un destino y valida la disponibilidad.
    Devuelve la cantidad solicitada si es válida o None si hay error.
    """
    try:
        cantidad = int(input("\nIndique la cantidad de reservas: "))
    except ValueError:
        print("\n❌ Error. Debe ingresar un numero entero\n")
        enter()
        return
    
    # Valido que haya suficientes lugares disponibles para la cantidad solicitada
    if cantidad > destino['disponibilidad']:
        print(f"\n❌ Lo sentimos, solo quedan {destino['disponibilidad']} lugares disponibles\n")
        enter()
        return
    elif cantidad <= 0:
        print("❌ Cantidad invalida. Debe ingresar al menos 1 reserva")
        enter()
        return
    
    return cantidad




def mostrar_menu():
    """
    Despliega el menu de opciones
    """

    print(f"""
        💵  Gestion de Ventas 💵
        
        1. Registrar Venta
        2. Listar Ventas
        3. Listar Ventas por Cliente
        4. Listar Ventas por Destino
        5. Modificar Precio de Venta
        6. Eliminar Venta
        7. Exportar Ventas a CSV
        0. Volver al Menu Principal
        """)
    


# Pausa para leer la informacion obtenida
def enter():
    """
    Pausa el programa para que el usuario lea la informacion obtenida antes de continuar.
    """
    input("\n⏹️   Presiona ENTER para continuar...")
        


def mostrar_clima_destino(nombre_destino):
    """
    Consulta y muestra el clima actual del destino usando la API de wttr.in.

    """
    try:
        # Construyo la URL de la API con el nombre del destino y en español
        url = f"https://wttr.in/{nombre_destino}?format=3&lang=es"

        # Hago la solicitud GET a la API y verifico que la solicitud sea exitosa
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            print(f"\n😉 Para ir entrando en 'clima'.. El clima actual en tu destino es: {respuesta.text}")
        else:
            print(f"\n⚠️ No se pudo obtener el clima de {nombre_destino.title()}.")

        # Capturo si hubo un error cuando intento hacer la solicitud
    except:
        print(f"\n⚠️ Error al consultar el clima")



"""
Funciones para CRUD de ventas:

"""
def registrar_venta():
    """
    Registra una nueva venta asociando un cliente con un destino y una cantidad de reservas.
    Actualiza la disponibilidad del destino y guarda la venta.
    """

    borrar()
    cliente = buscar_cliente_DNI()
    if cliente is None:
        return


    destino = seleccionar_destino()
    if destino is None:
        return
    
    # Muestro el clima actual del destino seleccionado
    mostrar_clima_destino(destino['nombre'])

    cantidad = solicitar_cantidad(destino)
    if cantidad is None:
        return

    # Calculo el precio total de la reserva despues de haber seleccionado la cantidad
    total = cantidad * destino["precio"]

    # Actualizo la cantidad de lugares disponibles en el diccionario
    destino['disponibilidad'] -= cantidad

    # Guardo los cambios en el json destinos
    guardar_destinos(destinos)
    print("\n✔️  Archivo de destinos actualizado con éxito.")

    # Fecha actual en formato dd/mm/yyyy
    fecha_venta = datetime.today().strftime("%d/%m/%Y")

    # Establezco el id de la venta
    if not ventas:
        id = 1
    else:
        id = max(v['id'] for v in ventas) + 1

    # Registrar la venta
    nueva_venta = {
        "id": id,
        "id_cliente": cliente["id"],
        "nombre_cliente": f"{cliente['nombre'].title()} {cliente['apellido'].title()}",
        "id_destino": destino["id"],
        "nombre_destino": destino["nombre"].title(),
        "cantidad": cantidad,
        "total": total,
        "fecha": fecha_venta
    }

    # Agrego la venta realizada al diccionario
    ventas.append(nueva_venta)

    # Guardo los cambios en el archivo json de ventas
    guardar_ventas(ventas)

    print("\n\t✅ Venta registrada con éxito! 🎉\n")

    print(f"""
    📑 Informe de la venta realizada: \n
        ID: {id}
        Cliente: {cliente['nombre'].title()} {cliente['apellido'].title()}
        Destino: {destino['nombre']}
        Cantidad: {cantidad}
        Total: $ {total}
        Fecha de venta: {fecha_venta}
        """)
    
    enter()




def listar_ventas():
    """
    Muestra una tabla con todas las ventas registradas en el sistema.
    """
    
    borrar()
    if not ventas:
        print("\n❌ No hay ventas registradas\n")
        enter()
        return
    
    tabla = []

    for v in ventas:

        fila = [v['id'], v["nombre_cliente"], v["nombre_destino"], v['cantidad'], f"$ {v['total']}", v['fecha']]
        tabla.append(fila)

    headers = ["Id Venta", "Cliente", "Destino", "Cantidad", "Total", "Fecha"]

    print("\n💵  Las Ventas registradas son: \n")
    print(tabulate(tabla, headers, tablefmt="fancy_grid"))
    enter()




def ventas_por_cliente():
    """
    Filtra y muestra todas las ventas realizadas por un cliente específico.
    """

    borrar()
    cliente = buscar_cliente_DNI()
    if cliente is None:
        enter()
        return

    ventas_cliente = []
    for v in ventas:
        if v['id_cliente'] == cliente['id']:
            ventas_cliente.append(v)

    if not ventas_cliente:
        print(f"\n❌ No hay ventas registradas para {cliente['nombre'].title()} {cliente['apellido'].title()}")
        enter()
        return

    tabla = []
    for v in ventas_cliente:

        fila = [v['id'], v["nombre_destino"], v['cantidad'], f"$ {v['total']}", v['fecha']]
        tabla.append(fila)

    headers = ["ID Venta", "Destino", "Cantidad", "Precio Total", "Fecha"]
    print(f"\n🧐💲 Ventas realizadas por {cliente['nombre'].title()} {cliente['apellido'].title()}:\n")
    print(tabulate(tabla, headers, tablefmt="fancy_grid"))
    enter()




def ventas_por_destino():
    """
    Filtra y muestra todas las ventas realizadas a un destino específico.
    """

    borrar()
    print("\n🗺️    La lista de destinos es: \n")
    mostrar_destinos()
    destino = buscar_destino_ID()
    if destino is None:
        enter()
        return

    ventas_destino = []
    for v in ventas:
        if v['id_destino'] == destino['id']:
            ventas_destino.append(v)

    if not ventas_destino:
        print(f"\n❌ No hay ventas registradas para el destino '{destino['nombre']}'")
        enter()
        return

    tabla = []
    for v in ventas_destino:

        fila = [v['id'], v["nombre_cliente"], v['cantidad'], f"$ {v['total']}", v['fecha']]
        tabla.append(fila)

    headers = ["ID Venta", "Cliente", "Cantidad", "Precio Total", "Fecha"]
    print(f"\n💵  Ventas realizadas al destino '{destino['nombre']}':\n")
    print(tabulate(tabla, headers, tablefmt="fancy_grid"))
    enter()




def modificar_total_venta():
    """
    Permite modificar el precio total de una venta ya registrada.
    """

    listar_ventas()
    try:
        id_modificar = int(input("\nIngrese el ID de la venta a modificar: "))
    except ValueError:
        print("\n❌ ID inválido. Debe ingresar un numero entero\n")
        enter()
        return


    for v in ventas:
        if v['id'] == id_modificar:

            try:
                nuevo_total = float(input("\nIngrese el precio total sin signo '$': "))

            except ValueError:
                print("\n❌ Precio inválido. Debe ingresar un número válido\n")
                enter()
                return
            
            # Modifico el monto total
            v['total'] = nuevo_total

            guardar_ventas(ventas)

            print("\n\t✅ Venta actualizada con éxito 🎉\n")
            print(f"💲 El nuevo precio total registrado es $ {v['total']:.2f}\n")
            return

    print("\n❌ Venta no encontrada\n")
    enter()




def eliminar_venta():
    """
    Elimina una venta por su ID y actualiza la disponibilidad del destino correspondiente.
    """
    
    borrar()
    print("\n Estas son las ventas registradas: \n")
    listar_ventas()
    try:
        id_eliminar = int(input("\nIngrese el ID de la venta a eliminar: "))
    except ValueError:
        print("\n❌ ID inválido. Debes ingresar un numero entero\n")
        enter()
        return


    for v in ventas:
        if v['id'] == id_eliminar:
            id_destino = v['id_destino']
            cantidad = v['cantidad']

            confirmar = input("\n🤔 ¿Está seguro que desea eliminar esta venta? (S / N): ").upper()
            if confirmar != 'S':
                print("\n❌ Operación cancelada\n")
                enter()
                return

            # Si la encuentra elimina esa venta
            ventas.remove(v)
            guardar_ventas(ventas)
            print("\n\t✅ Venta eliminada con éxito")
        
        
            # Actualizo la disponibilidad al destino
            for d in destinos:
                if d['id'] == id_destino:
                    d['disponibilidad'] += cantidad
                    guardar_destinos(destinos)
                    print(f"\n✔️  Disponibilidad de '{d['nombre']}' actualizada\n")
                    enter()
                    return
        
    print("\n❌ Venta no encontrada\n")
    enter()



def exportar_ventas_csv():
    """
    Exporta todas las ventas registradas a un archivo CSV llamado 'ventas.csv'.
    Si no hay ventas, muestra un mensaje de error y no crea el archivo.
    """
    if not ventas:
        print("\n❌ No hay ventas para exportar\n")
        enter()
        return

    with open("Archivos-exportados/ventas.csv", mode="w", newline="", encoding="utf-8") as archivo:
        campos = ["ID", "Cliente", "Destino", "Cantidad", "Total", "Fecha"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        escritor.writeheader()
        for v in ventas:
            escritor.writerow({
                "ID": v["id"],
                "Cliente": v["nombre_cliente"],
                "Destino": v["nombre_destino"],
                "Cantidad": v["cantidad"],
                "Total": v["total"],
                "Fecha": v["fecha"]
            })

    print("\n✅ Archivo 'ventas.csv' exportado con éxito! 🎉")
    enter()




"""
gestion_ventas() ==> FUNCION PRINCIPAL DEL MODULO VENTAS

"""

def gestion_ventas():
    """
    Función principal del módulo de ventas. Muestra el menú y ejecuta las operaciones correspondientes
    según la opción seleccionada por el usuario.
    """
    
# Muestra el menú cada vez que comienza el bucle
    while True:
        mostrar_menu()  

# try / except ==> Validación de entrada: Me aseguro con el except que el usuario ingrese un numero, sino le permite  reintentar
        try:
            seleccion = int(input("Selecciona una opcion del Menu Ventas (del 1 al 7): "))

        except ValueError:
            print("\n❌ Debes ingresar un numero del 1 al 7: ")
            continue

        match seleccion:
            case 1:
                registrar_venta()
            case 2:
                listar_ventas()
            case 3:
                ventas_por_cliente()
            case 4:
                ventas_por_destino()
            case 5:
                modificar_total_venta()
            case 6:
                eliminar_venta()
            case 7:
                exportar_ventas_csv()
            case 0:
                print("\n🔙  Volviendo al Menu..\n")
                break
            case _:
                print("\n❌ Opción inválida. Ingrese un número del 1 al 7\n")
                



"""
Permite ejecutar esta funcion directamente desde este archivo y evita que se ejecute automáticamente si lo importo desde otro módulo (menu)

"""
if __name__ == "__main__":
    gestion_ventas()

