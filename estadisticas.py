'''

Destinos mas vendidos, menos vendidos, etc


'''
import os
from datetime import datetime
import os.path
import json
from tabulate import tabulate

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def abrir_json(archivo):
    #el parametro archivo recibira, clientes para abrir el clientes.json, o ventas para abrir el ventas.json, o destinos para abrir destinos.json
    nombre_archivo=f"Archivos-Json/{archivo}.json"
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo,"rt",encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return f"Error: El archivo '{nombre_archivo}' no es un JSON válido."
    else:
        return f"no existe el archivo {archivo}.json"

def clienteById(id:int)->str: #devuelve nombre y apellido del cliente con el id cliente
    clientes=abrir_json('clientes')
    if isinstance(clientes, str):
        print(clientes)
        return []
    for cliente in clientes:
        if cliente.get("id") == id:
            return f'{cliente.get('nombre')} {cliente.get('apellido')}'
            
def dniById(id:int)->str: #devuelve dni del cliente con el id cliente
    clientes=abrir_json('clientes')
    if isinstance(clientes, str):
        print(clientes)
        return []
    for cliente in clientes:
        if cliente.get("id") == id:
            return f'{cliente.get('dni')}'

def destinoById(id:int)->str: #devuelve nombre del destino con el id destino
    destinos=abrir_json('destinos')
    if isinstance(destinos, str):
        print(destinos)
        return []
    for destino in destinos:
        if destino.get("id") == id:
            return f'{destino.get('nombre')}'

def mostrarVta(listaVta):
    lista=[]
    for l in listaVta:
        lista1={k:v for k,v in l.items() if k != 'id_cliente' and k != 'id_destino'}
        lista.append(lista1)    
    print(tabulate(lista, headers='keys', tablefmt='rst',stralign='center'))
    
def fecha_inicio_fin():
    i=True
    f=True
    while f:
        while i:
            try:
                perInicial=input("indique dia mes y año inicio en la forma dd/mm/yyyy: ")
                perInicialDT=datetime.strptime(perInicial, "%d/%m/%Y") #cambia la fecha a datetime       
                perFinal=input("indique dia mes y año fin en la forma dd/mm/yyyy: ")
                perFinalDT=datetime.strptime(perFinal, "%d/%m/%Y") #cambia la fecha a datetime
                i=False
            except Exception:
                limpiar_pantalla()
                print("Error: ingrese la fecha en el formato indicado")
        if perInicialDT > perFinalDT:
            limpiar_pantalla()
            i=True
            print('la fecha inicial tiene que ser menor que la fecha final')
        else:
            f=False
    return [perInicialDT,perFinalDT]

def ventasPorPeriodo():
    limpiar_pantalla() #limpia la pantalla
    print("elija el periodo")
    perInicialDT, perFinalDT=tuple(fecha_inicio_fin())
    print('\n')
    listaVta=[]
    ventas=abrir_json('ventas')
    if isinstance(ventas, str):
        print(ventas)
        return []
    for venta in ventas: #recorre los elementos buscando y guardando los que esten entre la fecha inicio y fin que ingresó el usuario
            fechaVentaDT=datetime.strptime(venta.get("fecha"), "%d/%m/%Y")
            if fechaVentaDT > perInicialDT and perFinalDT > fechaVentaDT:
                listaVta.append(venta)
    mostrarVta(listaVta)
        
            
def destinos():
    limpiar_pantalla() #limpia la pantalla
    print('indique la fecha para la busqueda')
    fechaInicioDT, fechaFinDT=tuple(fecha_inicio_fin())
    print('\n')
    #destino=abrir_json('destinos')
    ventas=abrir_json('ventas')
    if isinstance(ventas, str):
        print(ventas)
        return []
    destinos=abrir_json('destinos')
    if isinstance(destinos, str):
        print(destinos)
        return []
    listaIdDestino=[]
    for destinoId in ventas:
        id=destinoId['id_destino']
        if id not in listaIdDestino:
            listaIdDestino.append(id)
    for destinoId in destinos:
        id=destinoId['id']
        if id not in listaIdDestino:
            listaIdDestino.append(id)
    masVendido = {}#diccionario con los id de los destinos 
    for lista in listaIdDestino:
        masVendido[lista]= 0
    #ventas=abrir_json('ventas')
    for venta in ventas: #recorre las ventas, armando una lista de los mas vendidos
            fechaVtaDT=datetime.strptime(venta['fecha'], "%d/%m/%Y")
            if  fechaVtaDT > fechaInicioDT and fechaFinDT > fechaVtaDT:
                for idDestino in listaIdDestino:
                   if idDestino == venta.get('id_destino'):
                       masVendido[idDestino] += venta.get('cantidad')   
    return masVendido        
                

def destinosMasVendidos():
    masVendido = destinos()#destinos() trae una lista de diccionario con los destinos como clave y la cantidad vendida como valor
    if masVendido == []:
        return
    for item in dict(sorted(masVendido.items(), key=lambda item: item[1], reverse=True)):
            print(f'el destino {destinoById(item)} se vendio {masVendido[item]} veces')

def destinosMenosVendidos():
    menosVendido = destinos()
    if menosVendido == []:
        return
    for item in dict(sorted(menosVendido.items(), key=lambda item: item[1], reverse=False)):
            print(f'el destino {destinoById(item)} se vendio {menosVendido[item]} veces')

def ventasDeUnDestino():
    #tomar las ventas y sumar las que correspondan al destino elegido
    limpiar_pantalla()
    destinos=abrir_json('destinos')
    if isinstance(destinos, str):
        print(destinos)
        return []
    print('\n')
    ventas=abrir_json('ventas')
    if isinstance(ventas, str):
        print(ventas)
        return []
    lista_destinos= list({venta["nombre_destino"] for venta in ventas})
    lista_destinos= list({destino['nombre'] for destino in destinos})
    
    #valida que se ingrese una opcion valida
    try:
        while True:
            print("a continuacion tiene la lista de destinos disponible, elija su opcion para mostrar la cantidad vendida")
            contador=0
            for destino in lista_destinos:
                print(f'{contador+1}-{destino}')
                contador +=1

            idDestino = int(input("ingrese su opcion: "))
            #idDestino != None 
            if  idDestino > 0 and idDestino <= len(lista_destinos):
                break
            else:
                limpiar_pantalla()
                print('elija una entre las opciones disponibles')
    except Exception:
        limpiar_pantalla()
        print('elija una opcion valida')
        return 
    contarDestinos=0
    for venta in ventas:
        if venta.get('nombre_destino') == lista_destinos[idDestino-1]:
            contarDestinos += venta.get('cantidad')
    print(f'el destino {lista_destinos[idDestino-1]} se han vendido {contarDestinos} lugares')
    


def estadisticas():
    limpiar_pantalla()
    i=True
    while i:
                print("=======================Menu Estadisticas ==================================")
                print("1-Ventas por periodo")
                print("2-destinos mas vendidos")
                print("3-destinos menos vendidos")
                print("4-ventas de un destino")
                print("0-volver al menu anterior")
                opcion=input("elija su opcion: ")
                match opcion:
                    case '1':
                        ventasPorPeriodo()
                    
                    case '2':
                        destinosMasVendidos()
                    
                    case '3':
                        destinosMenosVendidos()
                    
                    case '4':
                        ventasDeUnDestino()
                    
                    case '0':
                        i=False
                    case _:
                        print("elija una opcion valida")
                        
                     
if __name__== '__main__':
    estadisticas()