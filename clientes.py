
import json
import os

ARCHIVO = 'Archivos-Json/clientes.json'

def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_datos(clientes):
    with open(ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(clientes, f, indent=4)

        

def validar_dni(dni):
    return dni.isdigit() and (7 <= len(dni) <= 8)


def validar_telefono(telefono):
     return telefono.isdigit() and (len(telefono) >=8)


def validar_email(email):
    if "@" not in email:
        return False
    return True

def validar_codigo_postal(codigo_postal):
     return  len(codigo_postal) >=4


def agregar_cliente():
    clientes = cargar_datos()
    nuevo_id = max([c['id'] for c in clientes], default=0) + 1
    apellido = input("Apellido: ")
    nombre = input("Nombre: ")

    dni = input("DNI: ")
    while not validar_dni(dni):
        print("DNI inválido. Debe tener entre 7 y 8 dígitos.")
        dni = input("DNI: ")

    telefono = input("Teléfono: ")
    while not validar_telefono(telefono):
        print("Teléfono inválido debe contener mas de 8 digitos")
        telefono = input("Teléfono: ")

    email = input("Email: ")
    while not validar_email(email):
        print("Email inválido.")
        email = input("Email: ")

    direccion = input("Dirección: ")
    ciudad = input("Ciudad: ")

    codigo_postal = input("Codigo_postal: ")
    while not validar_codigo_postal(codigo_postal):
        print("Codigo postal inválido, debe contener 4 o mas digitos ")
        codigo_postal = input("Codigo postal: ")


    provincia = input("Provincia: ")
    pais = input("País: ")

    clientes.append({
        'id': nuevo_id,
        'apellido': apellido,
        'nombre': nombre,
        'dni': dni,
        'telefono': telefono,
        'email': email,
        'direccion': direccion,
        'ciudad': ciudad,
        'codigo_postal': codigo_postal,
        'provincia': provincia,
        'pais': pais
    })
    guardar_datos(clientes)
    print(" Cliente agregado exitosamente.\n")



def listar_clientes():
    clientes = cargar_datos()
    if not clientes:
        print(" No hay clientes registrados.\n")
        return
    for c in clientes:
        print(
            f"ID: {c['id']} | Apellido: {c['apellido']} | Nombre: {c['nombre']} | DNI: {c['dni']} "
            f"| Tel: {c['telefono']} | Email: {c['email']} | Dirección: {c['direccion']} | Ciudad: {c['ciudad']} | "
            f"Código Postal: {c['codigo_postal']} | Provincia: {c['provincia']} | País: {c['pais']}"
        )
    print()



def buscar_cliente():
    clientes = cargar_datos()
    termino = input("Buscar por nombre, apellido o DNI: ").lower()
    encontrados = [
        c for c in clientes
        if termino in c['nombre'].lower() or
           termino in c['apellido'].lower() or
           termino in c['dni']
    ]
    if not encontrados:
        print(" No se encontró ningún cliente.\n")
    else:
        for c in encontrados:
            print(
                f"ID: {c['id']} | Apellido: {c['apellido']} | Nombre: {c['nombre']} | DNI: {c['dni']} "
                f"| Tel: {c['telefono']} | Email: {c['email']} | Dirección: {c['direccion']}, {c['ciudad']}, "
                f"{c['codigo_postal']}, {c['provincia']}, {c['pais']}"
            )
        print()



def eliminar_cliente():
    clientes = cargar_datos()
    id_input = input("Ingrese el ID del cliente a eliminar: ")
    if not id_input.isdigit():
        print("ID inválido.\n")
        return

    id_eliminar = int(id_input)
    cliente_encontrado = False
    for cliente in clientes:
        if cliente['id'] == id_eliminar:
            clientes.remove(cliente)
            guardar_datos(clientes)
            print("Cliente eliminado exitosamente.\n")
            cliente_encontrado = True
            break

    if not cliente_encontrado:
        print("No se encontró un cliente con ese ID.\n")

        
        
def modificar_cliente():
    clientes = cargar_datos()
    id_input = input("Ingrese el ID del cliente a modificar: ")
    
    if not id_input.isdigit():
        print("ID inválido.\n")
        return

    id_modificar = int(id_input)
    encontrado = False

    for cliente in clientes:
        if cliente['id'] == id_modificar:
            encontrado = True
            print("Deje vacío si no quiere modificar un campo.\n")
            for campo in ['apellido', 'nombre', 'dni', 'telefono', 'email', 'direccion', 'ciudad', 'codigo_postal', 'provincia', 'pais']:
                valor_actual = cliente[campo]
                nuevo_valor = input(f"{campo} [{valor_actual}]: ")
                if nuevo_valor:
                    cliente[campo] = nuevo_valor
            guardar_datos(clientes)
            print("Cliente modificado exitosamente.\n")
            break

    if not encontrado:
        print("No se encontró un cliente con ese ID.\n")        



def clientes():
    while True:
        print("=== Menú de Clientes ===")
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente")
        print("4. Eliminar cliente")
        print("5. Modificar Cliente")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            agregar_cliente()
        elif opcion == '2':
            listar_clientes()
        elif opcion == '3':
            buscar_cliente()
        elif opcion == '4':
            eliminar_cliente()
        elif opcion == '5':
            modificar_cliente()
        elif opcion == "6":  
            print(" Saliendo del programa.")
            break
        else:
            print(" Opción inválida. Intente de nuevo.\n")

if __name__ == "__main__":
    clientes()
