# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import shutil, os

from datetime import datetime, date, time
import calendar

#mongodb
import pymongo
from pymongo import MongoClient

import telegram

#tiempo
import pyowm

#emojis
from emoji import emojize

import socket   #socket
import select
import sys  #salir de la aplicacion
import fileinput #teclear valor de variables
import os #limpiar terminal
import time #tiempo de espera antes de mandar un ping
from cPickle import dump, dumps, load, loads
port_serv=10000

#Opciones en los menús
OBJETO, OPC, OPCIONES, MENU, RESPUESTA = range(5)

#Mensajes fijos
mensaje = "¿Desea algo más?"

#juego
game = "t.me/DeLaHorraBot?game=DeLaHorraGame"
#Número de objetos
obj = 1
pole = False
puerto = 5000
lista = list()


reply_keyboard1 = [['Si'], ['No']]

reply_keyboard2 = [['Lugar','Otros'],
                  ['Hecho']]

reply_keyboard3 = [['Tiempo', 'Publicidad'],
                  ['Objetos Perdidos'],
 		              ['Juego', 'Chat'],
                  ['Finalizar']]

reply_keyboard4 = ['start']
                  
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)

class objetoPerdido:
  idOb = ""
  lugar = ""
  otros = ""
  imagen = ""
  fecha = ""
  def __init__(idOb, place, mas, pic, mom):
    self.idOb = obj
    self.lugar = place
    self.otros = mas
    self.imagen = pic
    self.fecha = mom



#Pasar a cadenas de caracteres
def convertir(user_data):
    caracteristicas = list()

    for car, valor in user_data.items():
        
        caracteristicas.append('{} - {}'.format(car, valor))

    return "\n".join(caracteristicas).join(['\n', '\n'])
    
def pasarALista(user_data):
    caracteristicas = list()

    for car, valor in user_data.items():
        
        if(car == 'Lugar'):
          objetoPerdido.lugar = valor
          
        if(car == 'Otros'):
          objetoPerdido.otros = valor
        caracteristicas.append('{} - {}'.format(car, valor))

    #archivo = open(fichero)
    #archivo.write(caracteristicas)
    #archivo.close()
    return caracteristicas

def start(bot, update):
    update.message.reply_text(
        "Bienvenido " + str(update.message.chat.first_name) + ". ¿Qué desea?",
        reply_markup=markup3)
    update.message.reply_text(emojize(":robot_face:"))
    print(update.message.chat.id)
    return MENU


def car_obj(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text

    update.message.reply_text(
        '{}, ¿qué sabes sobre ello?'.format(text))
    return RESPUESTA

def hablar(bot, update, user_data):
  print("HAblar")
  global puerto

  ip = "3.85.166.166"

 # puerto_par=raw_input("puerto de escucha clientes nuevos 500")#puerto de escucha a otros clientes a partir del 5000
  puerto_par= puerto + 1

  print(puerto)
#nombre=raw_input("Introduce el nombre con el que apereceras en el chat : ")
  nombre = update.message.chat.first_name
#variables
  inputs=[]
#escucha de otros per
  escucha=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  escucha.setblocking(0)
  escucha.bind(('',puerto_par))
  escucha.listen(10)#escucha de otros clientes
  inputs.append(escucha)#ayadir socket a lista de descriptores

#descriptor server
  print'puerto servidor en : ', port_serv
  servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creacion de socket TCP
  inputs.append(servidor)
  servidor.connect((ip,port_serv))#solicitud de conexion al servidor
  print "conectando con servidor en "+ip+" , "+str(port_serv)
#descriptor nueva conexion y agrego todas las conexiones que forman el chat
  lista=servidor.recv(4096)
  cadena=""
  if lista!="0":
    lista_conexiones = loads(lista)
    print "La lista de conexiones recibida del servidor tiene ", str(len(lista_conexiones))," clientes:"
    for cad in lista_conexiones:
      print str(cad[0])+str(cad[1])
    for conex in lista_conexiones:#recorrer todas los clientes conectados al chat
      par = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      par.connect(conex)#conexion con otros peer
      inputs.append(par)#añadir socket de conexion a descriptores
      print "nueva conexion con peer : ", conex
  servidor.send(str(puerto_par))#ahora actualizo lista del server con mi direccion y puerto de escucha
#descriptor teclado
  teclado=sys.stdin
  inputs.append(teclado)
#interrupciones con select
  update.message.reply_text(nombre+":\t")
  while inputs:
    readable, writable, excepcion= select.select(inputs, [], [])
    for activada in readable:#recorrer lista de descriptores
      if activada is escucha:#preguntar:se trata de una peticion de conexion por parte de algun peer nuevo que se ha conectado al chat
        data,addr = activada.accept()# conexion aceptada
        print "conexion con nuevo par en :",addr
        inputs.append(data)#agregar socket a lista de descriptores
      #print nombre+":\n\t"
      
        update.message.reply_text(nombre+":\n\t")
      else:
        if activada is teclado: #preguntar:descriptor es entrada por teclado
          mensaje=raw_input()
          for conexion in inputs:#recorrer lista de los descriptores
            if conexion!=teclado and conexion!=escucha and conexion!=servidor:#Quedarse solo con los peers
              if mensaje==":q":#mandar :q a todos los clientes
                conexion.send(mensaje)
              else:# se trata de un mensaje normal
                conexion.send(nombre+":\n\t"+mensaje)
          if mensaje==":q":# desconctarse a parte del servidor
            servidor.send(mensaje+","+str(puerto_par))
            conexion.close()
            #sys.exit()
            update.message.reply_text(mensaje, reply_markup = markup3)
            return MENU
            #print nombre
          else:
            mensaje=activada.recv(4096)
          if mensaje==":q":# si un usuario envia :q nos cerramos esa conexion
          #print "Se ha desconectado :",activada.getsockname()[0]+", "+str(activada.getsockname()[1])
            update.message.reply_text("Se ha desconectado :",activada.getsockname()[0]+", "+str(activada.getsockname()[1]))
            activada.close()
            inputs.remove(activada)
          else:
          #print mensaje
            update.message.reply_text(mensaje)

def info(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("¡Bien! De momento sabemos:"
                              "{}"
                              "¿Quieres añadir o modificar algo?".format(
                                  convertir(user_data)), reply_markup=markup2)

    return OPCIONES
    #return IMAGEN



def hecho(bot, update, user_data):
    global obj
    if 'choice' in user_data:
        del user_data['choice']

    mongoClient = MongoClient('localhost', 27017)
    db = mongoClient.Objetos
    collection = db.objetos

    #print(user_data) 
    lista.append(pasarALista(user_data))
    #print(lista)

    formato = "%d/%m/%Y %H:%M"
    ahora = datetime.utcnow()
    objeto_datetime = datetime.strftime(ahora, formato)

    objetoPerdido.fecha = objeto_datetime

    update.message.reply_text("Las características del objeto son:"
                              "{}".format(convertir(user_data)))
    print(objetoPerdido.idOb)
    print(objetoPerdido.lugar)
    print(objetoPerdido.otros)
    print(objetoPerdido.imagen)
    print(objetoPerdido.fecha)


    mongoClient = MongoClient('localhost', 27017)
    db = mongoClient.Objetos
    collection = db.objetos
    collection.save({'num': objetoPerdido.idOb, 'imagen': objetoPerdido.imagen,
    'lugar': objetoPerdido.lugar, 'otros': objetoPerdido.otros, 'fecha': objetoPerdido.fecha})
    obj += 1 
    print(obj)
    update.message.reply_text(mensaje, reply_markup = markup3)
    return MENU

# def imagen(bot, update, user_data):
#     global esperando_archivo
#     print("Imagen")
#     update.message.reply_text("Seleccione la foto del objeto")
#     if esperando_archivo == 1:
#         file = bot.getFile(update.message.photo[-1].file_id)
#         filename = os.path.join('imagen', '{}.jpg'.format(photo_file.file_id))
#         photo_file.download(filename)
#         esperando_archivo = 0

#     update.message.reply_text("¿Qué característica del objeto desea añadir?", reply_markup=markup2)
#     return OPCIONES

def imagen(bot, update, user_data):
    global obj

    #print("Imagen")
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    user = update.message.from_user.first_name


    tam = str(update.message.photo[-1].file_size)

    name = "./imagen/" + user + '_' + str(obj) + '_imagen.jpg'
    objetoPerdido.idOb = obj
    objetoPerdido.imagen = name
    print(objetoPerdido.idOb)
    print(name)

    # user_location = update.message.location
    # print("Location of %s: %f / %f", user.first_name, user_location.latitude,
    #              user_location.longitude)
    #print("file_id: " + str(update.message.photo.file_id))
  #  print os.getcwd()
   # os.chdir("/home/administrador/Telegram-Bot/python-telegram-bot/imagen")
    newFile.download(name)
   
   
   # shutil.move(name, "imagen")
 
   # os.chdir("/home/administrador/Telegram-Bot/python-telegram-bot")
  #  newFile.download(name)
    #newFile.download('test.jpg')
    update.message.reply_text("¿Qué característica del objeto desea añadir?", reply_markup=markup2)
    return OPCIONES


def image(bot, update, user_data):
    print("Imagen")
    update.message.reply_text("??????????? ????")
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('imagen', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if img_has_cat(filename):
        update.message.reply_text("?? ???????? ???? ?????, ???????? ? ??????????.")
        new_filename = os.path.join('cats', '{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("???????, ????? ?? ??????????!") 
    
    update.message.reply_text("¿Qué característica del objeto desea añadir?", reply_markup=markup2)
    return OPCIONES


def finalizar(bot, update):
   
    update.message.reply_text("Muchas gracias por usar este bot :) "
                              "Nos vemos pronto " + str(update.message.chat.first_name))
    

    return ConversationHandler.END


def tiempo(bot, update, user_data):
  update.message.reply_text("El tiempo en Alcalá es de: ")

  owm = pyowm.OWM('702f3dbc0eac34c326e7f3b7ea4f7bbd')
  observation = owm.weather_at_place('Alcala de Henares, es')
  w = observation.get_weather()
  temperature = w.get_temperature('celsius')
  viento = w.get_wind()
  humedad = w.get_humidity()
  lluvia = w.get_rain()
  print(str(lluvia))



  update.message.reply_text("Temperatura máxima: %s ºC\nTemperatura mínima: %s ºC\nTemperatura actual: %s ºC"
    %(temperature['temp_max'], temperature['temp_min'], temperature['temp']))
  
  update.message.reply_text("Viento: %s" %(viento['speed']))

  update.message.reply_text("Humedad: "+ str(humedad) +"%")
  # weather = Weather(unit=Unit.CELSIUS)
  # print("3")
  # location = weather.lookup_by_location('burgos')
  # print("4")
  # condition = location.condition
  # forecasts = location.forecast
  # for forecast in forecasts:
  #   print(forecast.text)
  #   print(forecast.date)
  # #print(condition.text)
  update.message.reply_text(mensaje, reply_markup = markup3)
  return MENU

def publicidad(bot, update, user_data):
  mongoClient = MongoClient('localhost', 27017)
  db2 = mongoClient.Publicidad
  collection = db2.publicidad
  ofertas = collection.find()
  #for publi in range(0, items):
  print("conectado")
  num = 1
  for publi in ofertas:
    update.message.reply_text("%s: %s"%(publi['tienda'], publi['oferta']))

    nombre = "/home/ubuntu/Telegram_Bot/python-telegram-bot/publicidad/oferta_" + str(num) + ".jpg"
    print(nombre)
    #bot.send_photo(chat_id, photo = open(nombre, 'rb'))
    #update.message.send_photo(chat_id, photo = open(nombre, 'rb'))
    #update.send_photo(chat_id, photo = open(nombre, 'rb'))
    #update.send_photo(chat_id = chat_id, photo = open('./publicidad/oferta_1.jpg','rb'))
    num += 1

  update.message.reply_text(mensaje, reply_markup = markup3)
  return MENU


def objeto(bot, update, user_data):

  #db = mongoClient.Objetos

  update.message.reply_text("¿Has encontrado un objeto nuevo?", reply_markup = markup1)
  
  return OBJETO

def objeto_perdido(bot, update, user_data):
  #text = update.message.text
  #user_data['choice'] = text
  #print(text)
  update.message.reply_text("Envíe la foto del objeto")
  return OPC


def mostrar_objetos(bot, update, user_data):

  mongoClient = MongoClient('localhost', 27017)
  db3 = mongoClient.Objetos
  collection = db3.objetos
  objetos = collection.find()
  num = collection.find().count() -1

  if(num == 1):
    update.message.reply_text("Hay " + str(num) + " objeto perdido.")
  else:
    update.message.reply_text("Hay " + str(num) + " objetos perdidos.")

  for objeto in objetos:
    if(objeto['num'] == 0):
      print("")
    else:
      update.message.reply_text("%s encontrado en %s\n el %s\nObservaciones: %s\n"
       %(objeto['imagen'], objeto['lugar'], objeto['fecha'], objeto['otros']))
  #for obj, lug, mas, ima in objetos:
   # update.message.reply_text(obj, lug, mas, ima)
  #for objeto in range(0, obj):
   # update.message.reply_text("Objeto")

  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def juego(bot, update):
  update.message.reply_text(game)  

def pole(bot, update, user_data):
  global pole
  
  mongoClient = MongoClient('localhost', 27017)
  db = mongoClient.Pole
  collection = db2.pole


  fecha = datetime.datetime.now()
  hora = fecha.hour
 
  if(pole == True):
    update.message.reply_text("Se te han adelantado. Prueba otro día")
  else:
    if(hora >= 0):
      update.message.reply_text("POLEEEEEE")
      # num = collection.find()
      # for
      # if(update.message.chat.id )
      pole = True
  
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU
  

def unknown(bot, update, user_data):
  update.message.reply_text("Disculpe, no le he entendido.\n¿Me puede repetir su petición?",
                          reply_markup = markup3)
  return MENU

def admin(bot, update, user_data):


  if(update.message.chat.id == 781490117):
    update.message.reply_text("Bienvenido Diego a la administración del Bot.")
    mongoClient = MongoClient('localhost', 27017)
    db = mongoClient.Objetos
    collection = db.objetos
    objetos = collection.find()
    num = collection.find().count() -1

    formato = "%d/%m/%Y"
    ahora = datetime.utcnow()
    fecha1 = datetime.strftime(ahora, formato)
    
    fecha1 = fecha1.split("/")

    dia1 = fecha1[0]
    mes1 = fecha1[1]
    ano1 = fecha1[2]
        
    total_1 = ((int(mes1) - 1 )* 30) + int(dia1)
    for objeto in objetos:

      if(objeto['num'] == 0):
        print("")
      else:
        fechaObjeto = objeto['fecha']
        aux = objeto['num']
        print("Fecha")
        fecha2 = fechaObjeto.split(" ")
        print(fecha2[0])
        elem = fecha2[0].split("/")
        dia2 = elem[0]
        mes2 = elem[1]
        ano2 = elem[2]
        
        a = date(ano2, mes2, dia2)
        print(a)
        total_2 = ((int(mes2) - 1 ) * 30) + int(dia2)
        print(str(total_2))
        
        print(str(total_1))
        total = total_1 - total_2
        print(total)
        if(total >= 40):
          
          borrar = {'num': int(aux)}
          collection.delete_one(borrar)
        

  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def main():
    #print(obj)
    
    updater = Updater("699075137:AAFO_iZ-Fk6QOWM89WbA4iUGrnBAhuC93KE")
    bot = telegram.Bot(token="699075137:AAFO_iZ-Fk6QOWM89WbA4iUGrnBAhuC93KE")

    mongoClient = MongoClient('localhost', 27017)
    updater.start_polling()

    #updater.message.reply_text("HOLA")
    print("Iniciando bot")
    print(bot.get_me())
    dp = updater.dispatcher

    #update.message.reply_text("Bienvenido al @BotDeLaHorra", reply_markup = markup4)
    #bot.sendMessage(chat_id=update.message.chat_id, text="Bienvenido")
    #Menú
    menu = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                RegexHandler('^(hola|Hola|ey|Ey|HOLA|HELLO|hello|hi|que|qué)$', start)]
                 #RegexHandler('', start)]
                ,

        states={
            MENU: [RegexHandler('^Objetos Perdidos$',
                                    objeto, pass_user_data = True),
                      RegexHandler('^Tiempo',
                                    tiempo, pass_user_data = True),
                      RegexHandler('^Publicidad$',
                                    publicidad, pass_user_data = True),
                      RegexHandler('^Finalizar$', finalizar),

                      RegexHandler('^Chat$', hablar, pass_user_data = True),

		                  RegexHandler('^Juego$', juego),

		                  RegexHandler('^(Pole|pole|POLE)$', pole,
				                              pass_user_data = True),

                      RegexHandler('^AdminBot$', admin, pass_user_data = True),

                      RegexHandler('',
                                unknown, pass_user_data = True),
                            
                      

                       ],
            
            OBJETO: [RegexHandler('^Si$', objeto_perdido, pass_user_data = True,
                                    ),
                    RegexHandler('^No$', mostrar_objetos, pass_user_data=True
                    )
            ],

            OPCIONES: [RegexHandler('^(Objeto|Lugar|Color|Marca|Dimensiones|Otros)$',
                          car_obj,
                          pass_user_data=True),
                     # RegexHandler('^Imagen$', imagen, pass_user_data = True),
                      RegexHandler('^Hecho$', hecho, pass_user_data = True)
                          ],
            
            OPC: [MessageHandler(Filters.photo, imagen, pass_user_data = True)],

            RESPUESTA: [MessageHandler(Filters.text,
                                          info,
                                          pass_user_data=True),
                           ],

          
        },

        fallbacks=[RegexHandler('^Finalizar$', finalizar)],
        allow_reentry=[True]
    )

    dp.add_handler(menu)


    #Iniciar bot
    updater.start_polling()

    # ^C para parar
    updater.idle()


if __name__ == '__main__':
    main()
