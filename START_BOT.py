#!/usr/bin/env python3

import datetime
import os
from github import Github
import telebot

# Token del bot de Telegram
TOKEN = '6163656411:AAGGKO95U1PiZ7KG-WcTxZfW0f2uIZfCN2w'

# Crear instancia del bot
bot = telebot.TeleBot(TOKEN)

# Obtener la fecha actual
fecha_actual = datetime.datetime.now().strftime("%d/%m/%y")

# Autenticación en GitHub
# Reemplaza 'tu-token' con tu token de autenticación de GitHub
g = Github('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')

# Obtener el repositorio
repo = g.get_repo('rodyher/Registro-gastos')

# Descarga y actualizacion
archivo = repo.get_contents("data.txt")

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def agregar_gasto(descripcion, montos):
    # Abrir el archivo data.txt en modo de escritura y agregar el nuevo gasto
    with open('data.txt', "a") as archivo:
        for monto in montos:
            archivo.write(f"({fecha_actual}), {descripcion}, {monto}\n")
    actualizar()

def descargar_archivo():
    # Descargar el archivo
    contenido = archivo.decoded_content.decode('utf-8')
    # Guardar el archivo localmente
    with open('data.txt', 'w') as f:
        f.write(contenido)

def actualizar():
    sha = archivo.sha
    # Leer el contenido actual del archivo data.txt
    with open('data.txt', 'r') as file:
        contenido = file.read()
    repo.update_file('data.txt', 'Actualización de datos (Telegram Bot)', contenido, sha, branch='main')

def calcular_saldo():
    saldo = 0

    # Leer el archivo data.txt localmente
    with open('data.txt', "r") as archivo:
        for linea in archivo:
            parte = linea.strip().split(", ")
            monto = float(parte[2])
            if parte[1].startswith("ADD"):
                saldo += monto  # Sumar el monto al saldo actual si es un ingreso marcado con ADD
            else:
                saldo -= abs(monto)  # Restar el monto al saldo actual si es un gasto
    return saldo

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hola! Soy tu bot de gastos personales. Puedes usar los siguientes comandos:\n"
                          "/saldo - Ver tu saldo actual\n"
                          "/agregar - Agregar un nuevo gasto\n"
                          "/historial - Ver el historial de gastos"
                          "/agregar_fondos - Agregar fondos a tu saldo")

@bot.message_handler(commands=['saldo'])
def show_balance(message):
    saldo = calcular_saldo()
    bot.reply_to(message, f"Tu saldo actual es: {saldo:.2f}")

@bot.message_handler(commands=['agregar'])
def add_expense(message):
    bot.reply_to(message, "Por favor, ingresa la descripción y los montos del gasto, separados por comas. "
                          "Por ejemplo: Comida, 10, 20, 30")

@bot.message_handler(commands=['historial'])
def show_history(message):
    with open('data.txt', "r") as archivo:
        historial = {}  # Diccionario para almacenar los datos por fecha
        for linea in archivo:
            parte = linea.strip().split(", ")
            fecha = parte[0][1:-1]  # Obtener la fecha eliminando los paréntesis
            descripcion = parte[1]
            monto = parte[2]
            if fecha not in historial:
                historial[fecha] = []
            historial[fecha].append((descripcion, monto))

    history_str = ""
    for fecha, datos in historial.items():
        history_str += f"[ {fecha} ]\n"
        for descripcion, monto in datos:
            history_str += f"- {descripcion}: {monto}\n"
        history_str += "\n"
    bot.reply_to(message, history_str)

@bot.message_handler(commands=['agregar_fondos'])
def add_funds(message):
    bot.reply_to(message, "Por favor, ingresa el monto a agregar")

def actualizar():
    sha = archivo.sha
    # Leer el contenido actual del archivo data.txt
    with open('data.txt', 'r') as file:
        contenido = file.read()
    repo.update_file('data.txt', 'Actualización de datos (Telegram Bot)', contenido, sha, branch='main')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith("/agregar"):
        try:
            partes = message.text.split(", ")
            descripcion = partes[1]
            montos = [float(monto_str) for monto_str in partes[2:]]
            agregar_gasto(descripcion, montos)
            bot.reply_to(message, "Gasto agregado correctamente.")
        except:
            bot.reply_to(message, "Error al agregar el gasto. Por favor, asegúrate de ingresar la descripción y los montos correctamente.")
    elif message.text.startswith("/agregar_fondos"):
        try:
            monto = float(message.text.split(" ")[1])
            with open('data.txt', "a") as archivo:
                archivo.write(f"({fecha_actual}), ADD, {monto}\n")
            actualizar()
            bot.reply_to(message, f"Fondos agregados correctamente. Tu nuevo saldo es: {calcular_saldo():.2f}")
        except:
            bot.reply_to(message, "Error al agregar fondos. Por favor, ingresa un monto válido.")
    else:
        bot.reply_to(message, "Comando no reconocido. Usa /help para ver la lista de comandos disponibles.")

# Descargar el archivo data.txt
descargar_archivo()

# Iniciar el bot
bot.polling()

