#!/usr/bin/env python3

import datetime
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def actualizar():
    saldo = calcular_saldo()
    print()
    print("------------------------------------------------------")
    print()
    print(f"Dato agregado. Su saldo actual es {saldo:.2f}")
    print()
    print("------------------------------------------------------")
    print()
    input("Presione Enter para continuar...")
    main()
    
def mostrar_menu(saldo):
    print()
    print()
    print(f"Bienvenido al registro de datos, su saldo es {saldo:.2f}")
    print()
    print()
    print("-------------------------------------------------------")
    print()
    print("Por favor elija una opción:")
    print()
    print("1- Agregar nuevo gasto")
    print("2- Ver historial")
    print("3- Agregar fondos")
    print("4- Salir")
    print()
    print("-------------------------------------------------------")
    print()
    print()
    print()

def agregar_gasto():
    limpiar_consola()
    print()
    print()
    descripcion = input("Descripción:      ")
    print()
    print()

    # Inicializar una lista para almacenar los montos
    montos = []

    # Bucle para ingresar los montos de forma dinámica
    while True:
        monto_str = input("Monto:        S/  ")
        if monto_str == "":
            break
        # Reemplazar las comas por puntos para permitir el ingreso de decimales con coma
        monto_str = monto_str.replace(",", ".")
        monto = float(monto_str)
        if monto == int(monto):  # Verificar si el monto es un número entero
            monto = int(monto)  # Convertir a entero si es necesario
        montos.append(monto)

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now().strftime("%d/%m/%y")

    # Abrir el archivo data.txt en modo de escritura y agregar el nuevo gasto
    with open("data.txt", "a") as archivo:
        for monto in montos:
            archivo.write(f"({fecha_actual}), {descripcion}, {monto}\n")
    actualizar()


def calcular_saldo():
    saldo = 0
    with open("data.txt", "r") as archivo:
        for linea in archivo:
            parte = linea.strip().split(", ")
            monto = float(parte[2])
            if parte[1].startswith("ADD"):
                saldo += monto  # Sumar el monto al saldo actual si es un ingreso marcado con ADD
            else:
                saldo -= abs(monto)  # Restar el monto al saldo actual si es un gasto
    return saldo


def ver_historial():
    print()
    print("Historial de datos:")
    print()

    with open("data.txt", "r") as archivo:
        historial = {}  # Diccionario para almacenar los datos por fecha
        for linea in archivo:
            parte = linea.strip().split(", ")
            fecha = parte[0][1:-1]  # Obtener la fecha eliminando los paréntesis
            descripcion = parte[1]
            monto = parte[2]
            if fecha not in historial:
                historial[fecha] = []
            historial[fecha].append((descripcion, monto))

    for fecha, datos in historial.items():
        print(f"[ {fecha} ]")
        for descripcion, monto in datos:
            print(f"- {descripcion}: {monto}")
        print()
    print()
    input("Presione Enter para continuar...")

def dividir_gasto():
    print()
    Jackson = float(input("Ingresa el sueldo de Jackson: S/ "))
    Rodyher = float(input("Ingresa el sueldo de Rodyher: S/ "))
    print()
    print()
    print()
    monto_gasto = float(input("Ingresa el monto del gasto compartido: S/ "))
    porcentaje_Jackson = (Jackson / (Jackson + Rodyher)) * 100
    porcentaje_Rodyher = (Rodyher / (Jackson + Rodyher)) * 100
    pago_Jackson = (porcentaje_Jackson / 100) * monto_gasto
    pago_Rodyher = (porcentaje_Rodyher / 100) * monto_gasto

    fecha_actual = datetime.datetime.now().strftime("%d/%m/%y")
    
    limpiar_consola()
    print()
    print()
    print("-------------------------------------------------------")
    print()
    print(f"Para cubrir el gasto de S/ {monto_gasto}")
    print()
    print(f"- Jackson ({porcentaje_Jackson:.2f}%) debe pagar S/ {pago_Jackson:.2f}")
    print(f"- Rodyher ({porcentaje_Rodyher:.2f}%) debe pagar S/ {pago_Rodyher:.2f}")
    print()
    print("-------------------------------------------------------")

    confirmacion = input("Confirmando los datos... desea guardar los cambios? S/N: ")
    print()
    if confirmacion.upper() == "S":
        with open("data.txt", "a") as archivo:
            archivo.write(f"({fecha_actual}), ADD, {monto_gasto}\n")
        actualizar()
            
    else:
        limpiar_consola()
        print()
        print()
        print("Cambios descartados.")
        print()
        print()
        print()
        print()
        print()
        print()
        input("Presione Enter para continuar...")
    
    
def agregar_fondos():
    limpiar_consola()
    print()
    print()
    print("Opción 3 - Agregar fondos")
    print()
    print("Dividir gasto:")
    print()
    print()
    dividir_gasto()
    
def main():
    saldo = calcular_saldo()
    while True:
        mostrar_menu(saldo)
        opcion = input("Ingrese su opción: ")
        if opcion == "1":
            agregar_gasto()
        elif opcion == "2":
            ver_historial()
        elif opcion == "3":
            agregar_fondos()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            limpiar_consola()
            print()
            print()
            print("Opción no válida. Por favor, ingrese una opción válida.")
            print()
            print()
            print()
            print()
            print()
            print()
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    limpiar_consola()
    main()