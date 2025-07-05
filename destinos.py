import json
import os
import re

ARCHIVO = 'Archivos-Json/destinos.json'

# Limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Pausar pantalla
def pausar():
    input("\nPresione Enter para continuar...")

# Cargar destinos desde el archivo JSON
def cargar_destinos():
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# Guardar destinos en el archivo JSON
def guardar_destinos(destinos):
    with open(ARCHIVO, 'w') as f:
        json.dump(destinos, f, indent=4)

# Validar nombre de destino
def validar_nombre_destino(nombre):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
    return bool(re.fullmatch(patron, nombre))

# Agregar destino
def agregar_destino(destinos):
    limpiar_pantalla()
    print("=== Agregar Nuevo Destino ===")

    nombre = input("Ingrese el nombre del destino: ")
    while not validar_nombre_destino(nombre):
        print("El nombre solo puede contener letras, espacios y letras con tilde.")
        nombre = input("Ingrese el nombre del destino nuevamente: ")

    # Validar precio
    while True:
        try:
            precio = float(input("Ingrese el precio del paquete: "))
            if precio <= 0:
                print("El precio debe ser un número positivo.")
            else:
                break
        except ValueError:
            print("Número inválido.")

    # Validar cupos
    while True:
        try:
            cupo = int(input("Ingrese los cupos disponibles: "))
            if cupo < 0:
                print("Los cupos no pueden ser negativos.")
            else:
                break
        except ValueError:
            print("Número inválido.")

    nuevo_id = max([d["id"] for d in destinos], default=0) + 1

    nuevo_destino = {
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
        "disponibilidad": cupo
    }

    destinos.append(nuevo_destino)
    guardar_destinos(destinos)
    print(f"\nDestino '{nuevo_destino['nombre']}' agregado correctamente.")
    print(f"ID: {nuevo_destino['id']} | Lugar: {nuevo_destino['nombre']} | Precio: ${nuevo_destino['precio']} | Cupos: {nuevo_destino['disponibilidad']}")
    pausar()

# Listar todos los destinos
def listar_destinos(destinos):
    limpiar_pantalla()
    print("=== Lista de Destinos ===")
    if not destinos:
        print("No hay destinos cargados.")
    else:
        for d in destinos:
            print(f"ID: {d['id']:<3} | Lugar: {d['nombre']:<12} | Precio: ${d['precio']:<10,.2f} | Cupos: {d['disponibilidad']}")
    pausar()


# Listar destinos por precio
def listar_destinos_por_precio(destinos):
    limpiar_pantalla()
    print("=== Lista de Destinos por Precio (menor a mayor) ===")
    if not destinos:
        print("No hay destinos cargados.")
    else:
        destinos_ordenados = sorted(destinos, key=lambda d: d['precio'])
        #cabecera
        print(f"{'ID':<5} {'Lugar':<20} {'Precio':>12} {'Cupos':>8}")
        print("-" * 50)
        for d in destinos_ordenados:
            print(f"{d['id']:<5} {d['nombre']:<20} ${d['precio']:>10,.2f} {d['disponibilidad']:>8}")
    pausar()


# Eliminar destino por ID
def eliminar_destino(destinos):
    limpiar_pantalla()
    print("=== Eliminar Destino ===")
    listar_destinos(destinos)
    try:
        id_eliminar = int(input("\nIngrese el ID del destino a eliminar: "))
        destino = next((d for d in destinos if d["id"] == id_eliminar), None)

        if destino:
            print(f"\nDestino seleccionado:")
            print(f"ID: {destino['id']} | Lugar: {destino['nombre']} | Precio: ${destino['precio']}")
            confirmacion = input("\n¿Seguro que desea eliminar este destino? (S/N): ").strip().upper()

            if confirmacion == 'S':
                destinos.remove(destino)
                guardar_destinos(destinos)
                print("\nDestino eliminado con éxito.")
            else:
                print("\nEliminación cancelada.")
        else:
            print("\nNo se encontró un destino con ese ID.")
    except ValueError:
        print("ID inválido.")
    pausar()

# Modificar destino por ID
def modificar_destino(destinos):
    limpiar_pantalla()
    print("=== Modificar Destino por ID ===")
    try:
        destino_id = int(input("Ingrese el ID del destino a modificar: "))
    except ValueError:
        print("Debe ingresar un número entero.")
        pausar()
        return

    destino = next((d for d in destinos if d["id"] == destino_id), None)

    if not destino:
        print(f"No se encontró un destino con ID {destino_id}.")
        pausar()
        return

    print(f"\nDestino seleccionado:")
    print(f"ID: {destino['id']} | Lugar: {destino['nombre']} | Precio: ${destino['precio']} | Cupos: {destino['disponibilidad']}")

    confirmar = input("\n¿Desea modificar este destino? (S/N): ").strip().lower()
    if confirmar != 's':
        print("Modificación cancelada.")
        pausar()
        return

    # Modificar nombre
    nuevo_nombre = input("Ingrese el lugar: ")
    while not validar_nombre_destino(nuevo_nombre):
        print("Solo letras, espacios y letras con tilde.")
        nuevo_nombre = input("Ingrese el nombre nuevamente: ")

    # Modificar precio
    while True:
        try:
            nuevo_precio = float(input("Ingrese el precio: "))
            if nuevo_precio <= 0:
                print("El precio debe ser un número positivo.")
            else:
                break
        except ValueError:
            print("Número inválido.")

    # Modificar cupos
    while True:
        try:
            nuevo_cupo = int(input("Ingrese la cantidad de cupos: "))
            if nuevo_cupo < 0:
                print("Los cupos no pueden ser negativos.")
            else:
                break
        except ValueError:
            print("Número inválido.")

    # Actualizar datos
    destino['nombre'] = nuevo_nombre
    destino['precio'] = nuevo_precio
    destino['disponibilidad'] = nuevo_cupo

    guardar_destinos(destinos)
    print(f"\nDestino Modificado:")
    print(f"ID: {destino['id']} | Lugar: {destino['nombre']} | Precio: ${destino['precio']} | Cupos: {destino['disponibilidad']}")
    pausar()

# Buscar por nombre parcial o total
def buscar_destino(destinos):
    limpiar_pantalla()
    print("=== Buscar Destino por Nombre ===")
    termino = input("Ingrese el nombre o parte del nombre del destino: ").lower()

    resultados = [d for d in destinos if termino in d["nombre"].lower()]

    if resultados:
        print("\nResultados encontrados:")
        for d in resultados:
            print(f"ID: {d['id']} | Lugar: {d['nombre']} | Precio: ${d['precio']}")
    else:
        print("\nNo se encontraron destinos con ese nombre.")
    pausar()

# Buscar destino por ID
def buscar_destino_por_id(destinos):
    limpiar_pantalla()
    print("=== Buscar Destino por ID ===")
    try:
        id_buscar = int(input("Ingrese el ID del destino: "))
        destino = next((d for d in destinos if d["id"] == id_buscar), None)

        if destino:
            print(f"\nDestino encontrado:")
            print(f"ID: {destino['id']} | Lugar: {destino['nombre']} | Precio: ${destino['precio']}")
        else:
            print("\nNo se encontró un destino con ese ID.")
    except ValueError:
        print("ID inválido.")
    pausar()

# Menú principal
def menu_destinos():
    destinos = cargar_destinos()

    while True:
        limpiar_pantalla()
        print("=== Agencia de Viajes ===")
        print("1. Listar destinos")
        print("2. Agregar destino")
        print("3. Eliminar destino")
        print("4. Buscar destino por nombre")
        print("5. Buscar destino por ID")
        print("6. Modificar destino por ID")
        print("7. Listar destinos por precio")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            listar_destinos(destinos)
        elif opcion == '2':
            agregar_destino(destinos)
        elif opcion == '3':
            eliminar_destino(destinos)
        elif opcion == '4':
            buscar_destino(destinos)
        elif opcion == '5':
            buscar_destino_por_id(destinos)
        elif opcion == '6':
            modificar_destino(destinos)
        elif opcion == '7':
            listar_destinos_por_precio(destinos)
        elif opcion == '8':
            print("Gracias por usar el sistema de Agencia de Viajes.")
            print("=" * 50)
            break
        else:
            print("Opción inválida.")
            pausar()

# Ejecutar
if __name__ == "__main__":
    menu_destinos()
