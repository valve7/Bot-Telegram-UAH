# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

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

#matemáticas
from math import sin, cos, sqrt, atan2, radians

#números aleatorios
from random import randint

#Opciones en los menús
OBJETO, OPC, OPCIONES, MENU, RESPUESTA, FILTRO, SITIO, FILTRADO, MOSTRAR, PUBLI,MAS, INTRO, INTRO_SITIO, INTRO_IMAGEN, UBICACION, FRASE= range(16)

#Mensajes fijos
mensaje = "¿Desea algo más?"

#Número de objetos
obj = 1
pub = 1
fra = 1
anterior = 1

reply_keyboard1 = [['Si'], ['No'],
                    ['Buscar']]

reply_keyboard2 = [['Cosa'],
                    ['Otros'],
                  ['Terminado']]

reply_keyboard3 = [['Tiempo', 'Publicidad'],
                  ['Objetos Perdidos'],
 		              ['Juego', 'Chat'],
                  ['Ayuda'],
                  ['Finalizar']]

reply_keyboard4 = [['Ok'],
                  ['Filtrar']]

reply_keyboard5 = [['Tipo'],
                  ['Proximidad']]

reply_keyboard6 = [['Mostrar']]

reply_keyboard7 = [['Ver']]

reply_keyboard8 = [['Mas'],
                    ['Ok']]

reply_keyboard9 = [['Introducir datos']]

reply_keyboard10 = [['Introducir localizacion']]

reply_keyboard11 = [['Introducir imagen']]

reply_keyboard12 = [['Cercania']]

reply_keyboard13 = [['Filtrar distancia']]

reply_keyboard14 = [['Continuar']]

reply_keyboard15 = [['Tipo']]

reply_keyboard16 = [['Guardar frase'],
                    ['No guardar']]

reply_keyboard17 = [['Frase']]

reply_keyboard18 = [['Pole'],
                    ['Ruleta rusa'],
                    ['Mayor/Menor']]

reply_keyboard19 = [['Tiro'],
                    ['Salir']]
 
reply_keyboard20 = [['Mayor'],
                    ['Menor']] 
                    
reply_keyboard21 = [['Mayor/Menor'],
                    ['Salir']]                
                  
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)
markup5 = ReplyKeyboardMarkup(reply_keyboard5, one_time_keyboard=True)
markup6 = ReplyKeyboardMarkup(reply_keyboard6, one_time_keyboard=True)
markup7 = ReplyKeyboardMarkup(reply_keyboard7, one_time_keyboard=True)
markup8 = ReplyKeyboardMarkup(reply_keyboard8, one_time_keyboard=True)
markup9 = ReplyKeyboardMarkup(reply_keyboard9, one_time_keyboard=True)
markup10 = ReplyKeyboardMarkup(reply_keyboard10, one_time_keyboard=True)
markup11 = ReplyKeyboardMarkup(reply_keyboard11, one_time_keyboard=True)
markup12 = ReplyKeyboardMarkup(reply_keyboard12, one_time_keyboard=True)
markup13 = ReplyKeyboardMarkup(reply_keyboard13, one_time_keyboard=True)
markup14 = ReplyKeyboardMarkup(reply_keyboard14, one_time_keyboard=True)
markup15 = ReplyKeyboardMarkup(reply_keyboard15, one_time_keyboard=True)
markup16 = ReplyKeyboardMarkup(reply_keyboard16, one_time_keyboard=True)
markup17 = ReplyKeyboardMarkup(reply_keyboard17, one_time_keyboard=True)
markup18 = ReplyKeyboardMarkup(reply_keyboard18, one_time_keyboard=True)
markup19 = ReplyKeyboardMarkup(reply_keyboard19, one_time_keyboard=True)
markup20 = ReplyKeyboardMarkup(reply_keyboard20, one_time_keyboard=True)
markup21 = ReplyKeyboardMarkup(reply_keyboard21, one_time_keyboard=True)

class objetoPerdido:
  idOb = ""
  objeto = ""
  lugar = ""
  otros = ""
  imagen = ""
  fecha = ""
  def __init__(idOb, tipo, place, mas, pic, mom):
    self.idOb = obj
    self.objeto = tipo
    self.lugar = place
    self.otros = mas
    self.imagen = pic
    self.fecha = mom

class publi:
  tienda = "" 
  objeto = ""
  oferta = ""
  lugar = ""
  imagen = ""
  distancia = ""
  def __init__(ti, ob, of, lu, im, di):
    self.tienda = ti
    self.objeto = ob
    self.oferta = of
    self.lugar = lu
    self.image = im
    self.distancia = di

#Pasar a cadenas de caracteres
def convertir(user_data):
    caracteristicas = list()

    for car, valor in user_data.items():
        
        caracteristicas.append('{} - {}'.format(car, valor))

    return "\n".join(caracteristicas).join(['\n', '\n'])
    
# def pasarALista(user_data):
#     print("ENTra")
#     caracteristicas = list()
#     print("PASANDO")
#     for car, valor in user_data.items():
        
#         if(car == 'Objeto'):
#           objetoPerdido.objeto = valor
          
#         if(car == 'Otros'):
#           objetoPerdido.otros = valor
#         caracteristicas.append('{} - {}'.format(car, valor))
    
#     print("PASADO")
#     #archivo = open(fichero)
#     #archivo.write(caracteristicas)
#     #archivo.close()
#     return caracteristicas

def start(bot, update):
    update.message.reply_text(
        "Bienvenido " + str(update.message.chat.first_name) + ". ¿Qué desea?",
        reply_markup=markup3)
    update.message.reply_text(emojize(":robot_face:"))
    #bot.send_photo(chat_id = update.message.chat_id, photo=open(('./imagen/Diego_1_imagen.jpg').encode('utf-8'),'rb'))
    #update.message.reply_text(update.message.location.latitude)
   # print(update.message.chat.id)
    return MENU


def car_obj(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text

    if(text == 'Cosa'):
      update.message.reply_text('{}, ¿de qué tipo de objeto se trata? (Ej: reloj, gorro...)'.format(text))
    if(text == 'Otros'):
      update.message.reply_text('{}, ¿qué deseas añadir sobre el objeto?'.format(text))
    if(text == 'Introducir datos'):
      update.message.reply_text('Añade Tienda/Objeto/Oferta')
    if(text == 'Cercania'):
      update.message.reply_text('¿A qué distancia en metros?')
    if(text == 'Tipo'):
      update.message.reply_text('Tipo de objeto')
    if(text == 'Frase'):
      update.message.reply_text('Frase: ')
    return RESPUESTA

def buzon(bot, update, user_data):
  
  global fra
    
 # print("HABLAR")
  mongoClient = MongoClient('localhost', 27017)
  db = mongoClient.Frases
  collection = db.frases
  fra = collection.find().count()
  frases = collection.find()

  num = randint(1, fra)


  for frase in frases:
    if(num == frase['num']):
      update.message.reply_text(frase['frase'])

  update.message.reply_text("¿Te gustaría añadir una frase?", reply_markup = markup16)

  return FRASE


def guardar(bot, update, user_data):


  update.message.reply_text("Pulse Frase para continuar", reply_markup = markup17)
  return OPCIONES


def info(bot, update, user_data):

    global fra
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    print(user_data['choice'])
    del user_data['choice']
    print(user_data)
    print(category)
    if((category == 'Cosa') |(category == 'Otros')):
      #update.message.reply_text("¡Bien! De momento sabemos:"
       #                       "{}"
        #                      "¿Quieres añadir o modificar algo?".format(
         #                         convertir(user_data)), reply_markup=markup2)
      #update.message.reply_text("¡Bien! De momento sabemos: \n%s\n%s"%user_data['Cosa'], 
      #user_data['Otros'], replymarkup=markup2) 

      update.message.reply_text("¿Quieres añadir o modificar algo?", reply_markup = markup2)
      return OPCIONES
    
    if((category == 'Tipo')):
      #print(convertir(user_data))
      #update.message.reply_text(convertir(user_data))
      # print("TIPOOOOO")
      # print(user_data)
      #for car, valor in user_data.items():
      #publi.objeto = user.data['Tipo']
      #print(publi.objeto)
      update.message.reply_text("¿Ver?", reply_markup=markup7)

      return PUBLI  
    
    if(category == 'Continuar'):
      publi.objeto = user.data['Tipo']
      update.message.reply_text("¿Ver?", reply_markup=markup7)
      del user_data['Tipo']
    
    if((category == 'Introducir datos')):

      for car, valor in user_data.items():
        var = valor.split('/')
        publi.tienda = var[0]
        publi.objeto = var[1]
        publi.oferta = var[2]

      update.message.reply_text("Ahora localización", reply_markup =markup10)

      return INTRO_SITIO

    if((category == 'Cercania')):

     # del user_data['Buscar']
     # update.mesage.reply_text(convertir(user_data))
      for car, valor in user_data.items():
        publi.distancia = valor

      update.message.reply_text('Ver por cercanía', reply_markup = markup13)
      return MENU
    
    if((category == 'Buscar')):

      # for car, valor in user_data.items():
      #   #print(valor)
      #   #mostrar_objetos(bot, update, user_data, valor)
      #   update.message.reply_text("¿Mostrar?", reply_markup=markup6)
      #   #del user_data['Buscar']
      #   print(user_data)
      update.message.reply_text("¿Mostrar?", reply_markup=markup6)
      return MOSTRAR

    if((category == 'Frase')):

      mongoClient = MongoClient('localhost', 27017)
      db = mongoClient.Frases
      collection = db.frases
      fra = collection.find().count()
      fra += 1

      collection.save({'num': fra,'frase': user_data['Frase']})
      
      update.message.reply_text(mensaje, reply_markup = markup3)
      del user_data['Frase']
      return MENU


def hecho(bot, update, user_data):
    global obj
    if 'choice' in user_data:
        del user_data['choice']

    mongoClient = MongoClient('localhost', 27017)
    db = mongoClient.Objetos
    collection = db.objetos

    obj = collection.find().count()
    #print(user_data.items()) 


    for car, valor in user_data.items():

        if(car == 'Cosa'):
          objetoPerdido.objeto = valor
          
        if(car == 'Otros'):
          objetoPerdido.otros = valor


    formato = "%d/%m/%Y %H:%M"
    ahora = datetime.utcnow()
    objeto_datetime = datetime.strftime(ahora, formato)

    objetoPerdido.fecha = objeto_datetime

    collection.save({'num': objetoPerdido.idOb, 'imagen': objetoPerdido.imagen, 
    'cosa': objetoPerdido.objeto, 'lugar': objetoPerdido.lugar, 
    'otros': objetoPerdido.otros, 'fecha': objetoPerdido.fecha})
    obj += 1 
    print(obj)
    update.message.reply_text(mensaje, reply_markup = markup3)
    del user_data['Cosa']
    del user_data['Otros']
    return MENU


def imagen(bot, update, user_data):
    global obj

    #print("Imagen")
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    user = update.message.from_user.first_name


   # tam = str(update.message.photo[-1].file_size)

    name = "./imagen/" + user + '_' + str(obj) + '_imagen.jpg'
    objetoPerdido.idOb = obj
    objetoPerdido.imagen = name

 
    newFile.download(name)

    update.message.reply_text("Ubicación: ")
    #update.message.reply_text("¿Qué característica del objeto desea añadir?", reply_markup=markup2)
    #return OPCIONES
    return SITIO


def sitio(bot, update, user_data):

  posicion = (update.message.location.latitude, update.message.location.longitude)
  print(posicion)
  objetoPerdido.lugar = posicion

  update.message.reply_text("¿Qué característica del objeto desea añadir (obligatorio introducir Cosa)?", reply_markup=markup2)
  return OPCIONES



def publicidad(bot, update, user_data):
  mongoClient = MongoClient('localhost', 27017)
  db2 = mongoClient.Publicidad
  collection = db2.publicidad
  ofertas = collection.find()
  #for publi in range(0, items):
  
  num = 1
  for publi in ofertas:
    pos = publi['localizacion']

    update.message.reply_text("%s: %s"%(publi['tienda'], publi['oferta']))

    nombre = "./publicidad/oferta_" + str(num) + ".jpg"
    bot.send_location(chat_id = update.message.chat_id, latitude=pos[0], longitude=pos[1])
    bot.send_photo(chat_id = update.message.chat_id, photo=open((nombre).encode('utf-8'),'rb'))

    num += 1

  update.message.reply_text(mensaje, reply_markup = markup4)
#  return MENU
  return FILTRO

def tipo(bot, update, user_data):
  update.message.reply_text("Filtrado por tipo de objeto en oferta o por distancia:", 
  reply_markup = markup5)
  return FILTRADO

def filtrado_tipo(bot, update, user_data):
  update.message.reply_text("¿Qué objeto está buscando?")
  text = update.message.text
  user_data['choice'] = text
  print(text, user_data)
#  update.message.reply_text("Tipo", reply_markup = markup14)
#  return OPCIONES
  return RESPUESTA

def buscar_tipo(bot, update, user_data):
  #update.message.reply_text("Estas son las ofertas:")
  mongoClient = MongoClient('localhost', 27017)
  db2 = mongoClient.Publicidad
  collection = db2.publicidad
  ofertas = collection.find()
  #print("objeto: " + objeto)
  #print(publi.objeto)
  #print(user_data['Tipo'])
  for car, valor in user_data.items():
    objeto = valor
    # print("ESTAMOS AQUI")
    # print(objeto)
    # print(str(objeto.lower()))
  num = 1
  
  for publi in ofertas:
    #print(publi['oferta'])
    if(publi['objeto'].lower() == objeto.lower()):
      
      pos = publi['Localizacion']
      update.message.reply_text("%s: %s"%(publi['tienda'], publi['oferta']))

      nombre = "./publicidad/oferta_" + str(num) + ".jpg"
      bot.send_location(chat_id = update.message.chat_id, latitude=pos[0], longitude=pos[1])
      bot.send_photo(chat_id = update.message.chat_id, photo=open((nombre).encode('utf-8'),'rb'))

      num += 1
  
  if(num == 1):
    update.message.reply_text("Lo siento, no he encontrado nada.")

  
  # del user_data['Buscar']
  # del user_data['Tipo']
  del user_data
  update.message.reply_text(mensaje, reply_markup = markup3)
  return MENU


def filtrado_lugar(bot, update, user_data):
  update.message.reply_text("Envíe su ubiación")
  return UBICACION

def ubicacion(bot, update, user_data):
  posicion = (update.message.location.latitude, update.message.location.longitude)
  print(posicion)
  publi.lugar = posicion
  update.message.reply_text("Pulse el siguiente botón", reply_markup = markup12)
  #print(user_data)
  return OPCIONES

def distancia(bot, update, user_data):
  # print(publi.distancia)
  # print(publi.lugar)

  lat1 = publi.lugar[0]
  lon1 = publi.lugar[1]

  mongoClient = MongoClient('localhost', 27017)
  db = mongoClient.Publicidad
  collection = db.publicidad
  ofertas = collection.find()

  num = 1
  for publicidad in ofertas:

    pos = publicidad['localizacion']

    r = 6371000

    x = (int(pos[1]) - int(lon1) * cos((int(pos[0]) + int(lat1)) / 2))
    y = (int(pos[0]) - int(lat1))

    distancia = r * sqrt(x*x + y*y)

    if(int(distancia) < int(publi.distancia)):
      
      update.message.reply_text("%s: %s"%(publicidad['tienda'], publicidad['oferta']))

      nombre = "./publicidad/oferta_" + str(num) + ".jpg"
      bot.send_location(chat_id = update.message.chat_id, latitude=pos[0], longitude=pos[1])
      bot.send_photo(chat_id = update.message.chat_id, photo=open((nombre).encode('utf-8'),'rb'))

      num += 1

  update.message.reply_text(mensaje, reply_markup=markup3)

  return MENU

def objeto(bot, update, user_data):

  update.message.reply_text("¿Has encontrado un objeto nuevo?", reply_markup = markup1)
  
  return OBJETO

def objeto_perdido(bot, update, user_data):
  #text = update.message.text
  #user_data['choice'] = text
  #print(text)
  update.message.reply_text("Envíe la foto del objeto")
  return OPC

def buscar_objetos(bot, update, user_data):
  update.message.reply_text("¿Qué tipo de objeto ha perdido?")
  text = update.message.text
  user_data['choice'] = text
  
  #update.message.reply_text("Continuar", reply_markup = markup14)
  #return OPCIONES
  return RESPUESTA
  

def mostrar_objetos(bot, update, user_data):

  aux = 0
  #print(obj)
  print(user_data.items())
  mongoClient = MongoClient('localhost', 27017)
  db3 = mongoClient.Objetos
  collection = db3.objetos
  objetos = collection.find()
  num = collection.find().count() -1

  for car, valor in user_data.items():

    obj = valor
  obj = user_data['Buscar']
  print(obj.lower())


  print(user_data)
  for objeto in objetos:
    if(objeto['num'] == 0):
      print("")
    else:
      if(objeto['cosa'].lower() == obj.lower()):
        
        bot.send_photo(chat_id = update.message.chat_id, photo=open((objeto['imagen']).encode('utf-8'),'rb'))
        a = objeto['lugar']

        bot.send_location(chat_id = update.message.chat_id, latitude=a[0], longitude=a[1])
        update.message.reply_text("Encontrado el %s\nObservaciones: %s\n"
       %(objeto['fecha'], objeto['otros']))
        aux += 1
      
  if(aux == 0):
    update.message.reply_text("Ninguna coincidencia, siga buscando. ¡Ánimo!")

  update.message.reply_text(mensaje, reply_markup=markup3)
  del user_data['Buscar']
  return MENU


def finalizar(bot, update):
   
    update.message.reply_text("Muchas gracias por usar este bot :) "
                              "Nos vemos pronto " + str(update.message.chat.first_name))
    
    return ConversationHandler.END


def tiempo(bot, update, user_data):

  aux = 0

  update.message.reply_text("El tiempo en Alcalá es de: ")

  owm = pyowm.OWM('702f3dbc0eac34c326e7f3b7ea4f7bbd')
  observation = owm.weather_at_place('Alcala de Henares, es')
  #observation = owm.weather_at_place('Wrexham, uk')
  #observation = owm.weather_at_place('Helsinki, fi')
  w = observation.get_weather()
  temperature = w.get_temperature('celsius')
  viento = w.get_wind()
  humedad = w.get_humidity()
  nubes = w.get_clouds()

  update.message.reply_text("Temperatura máxima: %s ºC\nTemperatura mínima: %s ºC\nTemperatura actual: %s ºC"
    %(temperature['temp_max'], temperature['temp_min'], temperature['temp']))
  
  update.message.reply_text("Viento: %s" %(viento['speed']))

  update.message.reply_text("Humedad: "+ str(humedad) +"%")

  if((nubes < 10) & (aux == 0)):
    update.message.reply_text("Despejado")
    update.message.reply_text(emojize(":sun_with_face:"))
    aux = 1
  if((nubes > 40) & (humedad > 70) & (aux == 0)):
    update.message.reply_text("Lloviendo")
    update.message.reply_text(emojize(":cloud_with_rain:"))
    aux = 1
  if((nubes > 70) & (humedad > 70) & (temperature['temp'] < 0) & (aux == 0)):
    update.message.reply_text("Nevando")
    update.message.reply_text(emojize(":cloud_with_snow:"))
    aux = 1
  else:
    if(aux == 0):
      update.message.reply_text("Cubierto")
      update.message.reply_text(emojize(":cloud:"))

  update.message.reply_text(mensaje, reply_markup = markup3)
  return MENU

def juego(bot, update):
  update.message.reply_text("¿A qué quieres jugar?", reply_markup = markup18)
  return MENU


def pole(bot, update, user_data):
  
  si = 0
  mongoClient = MongoClient('localhost', 27017)
  db = mongoClient.Poles
  collection = db.poles
  poles = collection.find()

  formato = "%d/%m/%Y"
  ahora = datetime.utcnow()
  dia = datetime.strftime(ahora, formato)


  for pole in poles:
    fecha = pole['fecha']
    if(fecha == dia):
      nombre = pole['persona']
      si += 1

  if(si == 1):
    update.message.reply_text("Se te ha adelantado " + str(nombre) + ". Prueba otro día")
    bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/Ricciardo.png").encode('utf-8'), "rb"))
  else:
    update.message.reply_text("POLEEEEEE")
    bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/Vettel.png").encode('utf-8'), "rb"))
    collection.save({'fecha': dia, 'persona': str(update.message.chat.first_name)})

  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU
 
def ruleta(bot, update, user_data):
  numero = randint(1,6)

  if(numero == 1):
    update.message.reply_text(emojize(":skull:"))
    update.message.reply_text(mensaje, reply_markup=markup3)
  else:
    update.message.reply_text("Has salido vivo de esta")
    update.message.reply_text("¿Quieres probar otro tiro o salir con vida?", reply_markup=markup19)
  
  return MENU

def mayor_juego(bot, update, user_data):
  global anterior
  anterior = randint(1,10)
  ruta = './cartas/' + str(anterior) + '.jpg'
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open((ruta).encode('utf-8'), "rb"))
  update.message.reply_text("¿Mayor o menor?", reply_markup=markup20)
  return MENU

def mayor(bot, update, user_data):
  global anterior
  numero = randint(1,10)
  ruta = './cartas/' + str(numero) + '.jpg'
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open((ruta).encode('utf-8'), "rb"))
  if(numero > anterior):
    update.message.reply_text("You win!")
  else:
    update.message.reply_text("Has fallado, suerte para la próxima")
  
  update.message.reply_text("Seguir jugando o salir", reply_markup=markup21)
  return MENU


def menor(bot, update, user_data):
  global anterior
  numero = randint(1,10)
  ruta = './cartas/' + str(numero) + '.jpg'
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open((ruta).encode('utf-8'), "rb"))
  if(numero < anterior):
    update.message.reply_text("You win!")
  else:
    update.message.reply_text("Has fallado, suerte para la próxima")
  
  update.message.reply_text("Seguir jugando o salir", reply_markup=markup21)
  return MENU

def ayuda(bot, update, user_data):
  update.message.reply_text("Este bot te permite realizar las acciones que se encuentran en el teclado del menú. "+
                    "Además, tiene los juegos como son la pole (pole) o la ruleta rusa (ruleta)")

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
        
        #a = date(ano2, mes2, dia2)
        #print(a)
        total_2 = ((int(mes2) - 1 ) * 30) + int(dia2)
        print(str(total_2))
        
        print(str(total_1))
        total = total_1 - total_2
        print(total)
        if(total >= 40):
          
          borrar = {'num': int(aux)}
          collection.delete_one(borrar)
 
  #print("HECHO")
  update.message.reply_text("¿Quieres añadir publicidad?", reply_markup = markup8)
  return MAS
 
def mas(bot, update, user_data):       

  update.message.reply_text("Vamos a añadir publicidad")
  update.message.reply_text("Introduce el nombre de la tienda, el tipo de objeto y la oferta en el",
   reply_markup = markup9)

  #print(user_data)
  return OPCIONES

# def intro_dat(bot, update, user_data):
 
#   print(user_data)


#   update.message.reply_text(mensaje, reply_markup=markup3)
#   return MENU

def intro_loc(bot, update, user_data):

  # print(publi.objeto)
  # print(publi.tienda)
  # print(publi.oferta)

  posicion = (update.message.location.latitude, update.message.location.longitude)
  print(posicion)
  publi.lugar = posicion

  update.message.reply_text("Introduce imagen de la oferta", reply_markup= markup11)
  return INTRO_IMAGEN

def intro_ima(bot, update, user_data):

  global pub

  mongoClient = MongoClient('localhost', 27017)
  db = mongoClient.Publicidad
  collection = db.publicidad

  pub = collection.find().count()

  file_id = update.message.photo[-1].file_id
  newFile = bot.getFile(file_id)

  name = "./publicidad/oferta_" +str(pub) + '.jpg'
  publi.imagen = name
  
  collection.save({'tienda': publi.tienda, 'objeto': publi.objeto, 
    'oferta': publi.oferta, 'localizacion': publi.lugar, 
    'imagen': publi.imagen})
  print(name)

  newFile.download(name)

  pub += 1
  update.message.reply_text(mensaje, reply_markup=markup3)
  del user_data['Introducir datos']
  return MENU

def bot_DHM(bot, update, user_data):
  update.message.reply_text("¿Todo bien? " + str(update.message.chat.first_name))
  update.message.reply_text("He sido programado por Diego de la Horra, espero que te guste cómo funciono")
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def fiesta(bot, update, user_data):
  update.message.reply_text("¿He oído fiesta??????? Me apunto.")
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/fiesta.jpg").encode('utf-8'), "rb")) 
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def que_tal(bot, update, user_data):
  update.message.reply_text("Los bots siempre estamos bien, no somos personas.")
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/bien.jpg").encode('utf-8'), "rb")) 
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def comida(bot, update, user_data):
  update.message.reply_text("¿¿Comida?? No tengo hambre, gracias.")
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/comida.jpg").encode('utf-8'), "rb")) 
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def gracias(bot, update, user_data):
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/gracias.jpg").encode('utf-8'), "rb")) 
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def perdon(bot, update, user_data):
  update.message.reply_text("El débil nunca puede perdonar. El perdón es el atributo de los fuertes.")
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/perdon.jpg").encode('utf-8'), "rb")) 
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def dinero(bot, update, user_data): 
  update.message.reply_text("El oro circula porque tiene valor, pero el papel moneda tiene valor porque circula")
  bot.send_sticker(chat_id = update.message.chat_id, sticker=open(("./stickers/dinero.jpg").encode('utf-8'), "rb")) 
  update.message.reply_text(mensaje, reply_markup=markup3)
  return MENU

def main():
    
    updater = Updater("699075137:AAFO_iZ-Fk6QOWM89WbA4iUGrnBAhuC93KE")
    bot = telegram.Bot(token="699075137:AAFO_iZ-Fk6QOWM89WbA4iUGrnBAhuC93KE")

    mongoClient = MongoClient('localhost', 27017)

    updater.start_polling()

    #print("Iniciando bot")
    print(bot.get_me())
   # print(time.time(), time.clock())

    dp = updater.dispatcher

    #update.message.reply_text("Bienvenido al @BotDeLaHorra", reply_markup = markup4)
    #bot.sendMessage(chat_id=update.message.chat_id, text="Bienvenido")
    #Menú
    menu = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                RegexHandler('^(hola|Hola|ey|Ey|HOLA|HELLO|hello|hi)$', start),
                RegexHandler('^(hola bot|Hola bot|hola Bot|Hola Bot|Buenos días|buenas|Buenas)$', start)

                 #RegexHandler('', start)]
                ],

        states={
            MENU: [RegexHandler('^Objetos Perdidos$', objeto, pass_user_data = True),
                      RegexHandler('^Tiempo', tiempo, pass_user_data = True),
                      RegexHandler('^Publicidad$', publicidad, pass_user_data = True),
                      RegexHandler('^Finalizar$', finalizar),
                      RegexHandler('^Chat$', buzon, pass_user_data = True),

                      RegexHandler('.{0,100}(fiesta).{0,100}$', fiesta, pass_user_data = True),
                      RegexHandler('.{0,100}(.u. tal).{0,100}$', que_tal, pass_user_data=True),
                      RegexHandler('.{0,100}(comida).{0,100}$', comida, pass_user_data = True),
                      RegexHandler('.{0,100}(racias).{0,100}$', gracias, pass_user_data = True),
                      RegexHandler('.{0,100}(erdona).{0,100}$', perdon, pass_user_data=True),
                      RegexHandler('.{0,100}(inero).{0,100}$', dinero, pass_user_data=True),

		                  RegexHandler('^Juego$', juego),

		                  RegexHandler('^(Pole|pole|POLE)$', pole, pass_user_data = True),

                      RegexHandler('^AdminBot$', admin, pass_user_data = True),

                      RegexHandler('^(DeLaHorraBot)$', bot_DHM, pass_user_data = True),

                      RegexHandler('^(Filtrar distancia)$', distancia, pass_user_data = True),

                      RegexHandler('^(Ayuda)$', ayuda, pass_user_data = True),

                      RegexHandler('^(Ruleta rusa|ruleta rusa|Tiro)$', ruleta, pass_user_data = True),
                      RegexHandler('^(Mayor/Menor)$', mayor_juego, pass_user_data = True),
                      RegexHandler('^(Mayor)$', mayor, pass_user_data = True),
                      RegexHandler('^(Menor)$', menor, pass_user_data = True),

                      RegexHandler('^(Salir)$', start),

                      RegexHandler('', unknown, pass_user_data = True),

                       ],
            
            OBJETO: [RegexHandler('^Si$', objeto_perdido, pass_user_data = True,),
                    RegexHandler('^Buscar$', buscar_objetos, pass_user_data=True),
                    RegexHandler('^No$', start)
            ],

            OPCIONES: [RegexHandler('^(Cosa|Otros|Introducir datos|Cercania|Continuar|Frase)$',
                          car_obj,
                          pass_user_data=True),
                     # RegexHandler('^Imagen$', imagen, pass_user_data = True),
                      RegexHandler('^Terminado$', hecho, pass_user_data = True)

                          ],
            SITIO: [MessageHandler(Filters.location, sitio, pass_user_data = True)],
            OPC: [MessageHandler(Filters.photo, imagen, pass_user_data = True)],

            FILTRO: [RegexHandler('^Ok$', start),
                RegexHandler('^Filtrar$', tipo, pass_user_data = True)],

            MOSTRAR: [RegexHandler('^Mostrar$', mostrar_objetos, pass_user_data = True)],
            PUBLI:[RegexHandler('^Ver$', buscar_tipo , pass_user_data = True)],
            FILTRADO: [RegexHandler('^(Proximidad)$', filtrado_lugar, pass_user_data = True),
                      RegexHandler('^Tipo$', filtrado_tipo, pass_user_data = True)
                    ],
            UBICACION: [MessageHandler(Filters.location, ubicacion, pass_user_data = True)],

            RESPUESTA: [MessageHandler(Filters.text, info, pass_user_data=True),
                           ],
            MAS: [RegexHandler('^Mas$', mas, pass_user_data = True),
                  RegexHandler('^Ok$', start)],

        #    INTRO: [RegexHandler('^Introducir datos$', intro_dat, pass_user_data = True)],
                  # RegexHandler('^Introducir localizacion$', intro_loc, pass_user_data = True),
            INTRO_IMAGEN:[MessageHandler(Filters.photo, intro_ima, pass_user_data = True)],
            INTRO_SITIO:[MessageHandler(Filters.location, intro_loc, pass_user_data = True)],

            FRASE: [RegexHandler('^(Guardar frase)$', guardar, pass_user_data = True),
                    RegexHandler('^(No guardar)$', start)],
          
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
