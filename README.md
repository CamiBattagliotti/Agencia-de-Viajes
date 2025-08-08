
<div align="center">

# 🛫 Sistema de Gestión de Viajes Turísticos 🛬

<br>

![Turismo](https://media1.tenor.com/m/hiC6FxfEFwcAAAAd/pandb-travel.gif)

</div>

<br>

> Proyecto final de Programación 1    
> Año: 2025


---

## Descripción

Este sistema de gestión de viajes está desarrollado en Python y permite trabajar con información de clientes, destinos turísticos, ventas y estadísticas.  

A través de un menú interactivo, podés cargar nuevos datos, buscar información, registrar ventas y consultar reportes de manera sencilla.  

Todos los datos se guardan en archivos `.json`, lo que permite mantener la información organizada y accesible entre sesiones.


---

## Estructura de Archivos

```
Proyecto/
│
├── Archivos-Json/
│   ├── clientes.json
│   ├── destinos.json
│   └── ventas.json
│
├── main.py
├── ventas.py
├── destinos.py
├── clientes.py
├── estadisticas.py
└── README.md
```

---

## Funcionalidades Principales

### 👤 Clientes

Desde el menú de clientes vas a poder:

- Cargar nuevos clientes  
- Buscar clientes por ID  
- Listar todos los clientes registrados  
- Eliminar un cliente existente  
- Modificar los datos de un cliente 

---

### 🗺️ Destinos

En el apartado de destinos se puede:

- Listar todos los destinos disponibles  
- Agregar nuevos destinos turísticos  
- Eliminar destinos que ya no estén activos  
- Buscar destinos por nombre o por ID  
- Modificar información de un destino  
- Ordenar destinos por precio para compararlos fácilmente  

---

### 💰 Ventas

El módulo de ventas permite:

- Registrar nuevas ventas de paquetes turísticos  
- Ver todas las ventas realizadas  
- Consultar ventas asociadas a un cliente específico  
- Consultar ventas por destino  
- Modificar el precio de una venta registrada  
- Eliminar ventas  
- Exportar todas las ventas a un archivo CSV para abrirlo con Excel (ventas.csv)
- Consultar y mostrar el **clima actual** del destino seleccionado al registrar una venta usando la API de [wttr.in](https://wttr.in)

### 🌤️ Consulta de clima en el destino

Al registrar una nueva venta, el sistema hace una consulta en tiempo real a la API de wttr.in y muestra el clima actual del destino turístico seleccionado, brindando información relevante al usuario antes de finalizar la venta.

---

### 📊 Estadísticas

La sección de estadísticas ofrece análisis como:

- Ventas realizadas entre dos fechas  
- Destinos más vendidos  
- Destinos menos vendidos  
- Ventas acumuladas de un destino en particular  

---

## Requisitos Técnicos

- **Python 3.x**
- Módulos estándar:
  - `datetime`
  - `os`
  - `json`
- Módulo adicional:
  - `tabulate`  
    Instalar con:
    ```
    pip install tabulate
    ```
  - `requests`  
    Instalar con:
    ```
    pip install requests

---


## 📚 Aprendizajes Aplicados

- Manipulación de archivos JSON en Python
- Manejo de fechas con `datetime`
- Uso de listas, diccionarios y funciones
- Modularización del código
- Manejo de errores con `try/except`
- Validación de entradas de usuario
- Generación de reportes y estadísticas
- Exportación de datos a archivos CSV
- Consumo de APIs externas en Python usando `requests`

---

## 📌 Créditos

Este proyecto fue realizado como entrega final para  **Programación 1**.
 
Institución: Universidad Nacional de Entre Rios 

Tecnicatura Universitaria en Desarrollo Web 

Integrantes: Carlos Gabrovich. Sebastian Guido. Paola Peñalva Rebaque. Bruno Bonelli. Camila Battagliotti.

Año: 2025

---

¡Gracias por visitar! 🌍✈️
