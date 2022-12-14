# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64 # modulo para codificar contenido binario y decodificarlo en uun String
import time as t
import socket as sck
import threading as th
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from streamlit.runtime.scriptrunner import add_script_run_ctx


#Variables globales para grafico Tiempos de Activacion de la Rutina
UDPServerSocket = None
bytesAddressPair = None
reply = None
server = None

if 'rutinaCargada' not in st.session_state:
  st.session_state.rutinaCargada = False  

if 'rutinaEjecutada' not in st.session_state:
  st.session_state.rutinaEjecutada = False  

if 'rutinaDatos' not in st.session_state:
  st.session_state.rutinaDatos = None  

if 'tiemposRespuesta' not in st.session_state:
  st.session_state.tiemposRespuesta = []  

if 'servidorStart' not in st.session_state:
  st.session_state.servidorStart = False 

if 'imagen1' not in st.session_state:
  with open('./Images/utnfrsf.png','rb') as archivo:
      contenido = archivo.read()
      st.session_state.imagen1= base64.b64encode(contenido).decode('utf-8')

if 'imagen2' not in st.session_state:
  with open('./Images/logoprogpostitulacion.png','rb') as archivo:
      contenido = archivo.read()
      st.session_state.imagen2= base64.b64encode(contenido).decode('utf-8') 

if 'imagen3' not in st.session_state:
  with open('./Images/cclicense.png','rb') as archivo:
      contenido = archivo.read()
      st.session_state.imagen3= base64.b64encode(contenido).decode('utf-8')   

if 'cssContent' not in st.session_state:
  with open("./CSS/estilos.css") as formatos:
    st.session_state.cssContent = f'<style>{formatos.read()}</style>'

# def iniciarServidorSimulador(session):
#   global UDPServerSocket
#   global bytesAddressPair
  
#   localPort   = 4022
#   bufferSize  = 128
 
#   # Create a datagram socket
#   UDPServerSocket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
#   UDPServerSocket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
#   UDPServerSocket.setsockopt(sck.SOL_SOCKET, sck.SO_BROADCAST, 1)

#   # Bind to address and ip
#   try:
#     UDPServerSocket.bind((sck.gethostbyname(sck.gethostname()), localPort))
#   except sck.socket.error as e:
#     print(str(e))
    
#   print("UDP server up and listening")
#   # Queda a la espera del ingreso de Datagramas
#   while(True):
#       try:
#         bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#         message = bytesAddressPair[0]
#         address = bytesAddressPair[1]
#         print("Mensaje Recibido: {!r}".format(message))
#       except sck.error as e:
#         print(str(e)) 
       
#       clientMsg = str(message,'UTF-8')
#       print(clientMsg)
#       #Aca deberiamos esperar que el usuario haga clic en el boton correspondiente
#       pos_inic = 0
#       pos_fin = clientMsg.index("#")
#       nroDisp = clientMsg[pos_inic:pos_fin]
      
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       tmax = int(clientMsg[pos_inic:pos_fin])  
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       crojo = clientMsg[pos_inic:pos_fin] 
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       cverde = clientMsg[pos_inic:pos_fin] 
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       cazul = clientMsg[pos_inic:pos_fin] 
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       tono = int(clientMsg[pos_inic:pos_fin])
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       distCM = int(clientMsg[pos_inic:pos_fin])
#       pos_inic = pos_fin+1
#       pos_fin = clientMsg.index("#", pos_inic)
#       resp = ("1"==clientMsg[pos_inic:pos_fin]) 
#       print(nroDisp + ' - ' + str(tmax) + ' - ' + crojo + ',' + cverde + ',' + cazul + ' - ' + str(tono) + ' - ' + str(distCM) + ' - ' + str(resp))
      
#       if(nroDisp=="1"):
#         simDisp = session.simDispositivo1
#       elif(nroDisp=="2"):
#         simDisp = session.simDispositivo2
#       elif(nroDisp=="3"):
#         simDisp = session.simDispositivo3
#       elif(nroDisp=="4"):
#         simDisp = session.simDispositivo4
#       elif(nroDisp=="5"):
#         simDisp = session.simDispositivo5
#       elif(nroDisp=="6"):
#         simDisp = session.simDispositivo6
#       elif(nroDisp=="7"):
#         simDisp = session.simDispositivo7
#       else:
#         simDisp = session.simDispositivo8
        
#       if(crojo=="255"):
#         #prende luz roja
#         simDisp[2] = "Roja"
#       elif(cverde=="255"):
#           #prende luz verde
#           simDisp[2] = "Verde"
#       else:
#           simDisp[2] = "Apagado"
      
#       if(resp=="1"):  #Veo si tengo que retornar o no una respuesta 
#         simDisp[4] = True
#       else:
#         simDisp[4] = False
      
#       simDisp[3] = False #Habilita el botón al usuario 
#       #Ahora hay que esperar que el usuario haga clic en el boton
#       ahora =dt.datetime.now() #obtengo fecha y hora actual del sistema
#       horaInicioDisp = dt.datetime.now().time()  #Obtengo solo la hora
#       deltaTmax = dt.timedelta(milliseconds=tmax)
#       horaMaxActivacion = (ahora + deltaTmax).time() # sumo la cantidad de milisegundos que espero activacion del usuario
#       activado = False
#       while   dt.datetime.now().time() <= horaMaxActivacion:
#         if simDisp[5] is not None:
#           #Envio mensaje respuesta - ver datetime.time
#           horaActivacion = dt.datetime(simDisp[5])
#           deltaT = (horaActivacion-horaInicioDisp).total_seconds()*1000
#           mensajeResp = nroDisp + "#" + str(deltaT) + "##"
#           bytesTrasmitidos = UDPServerSocket.sendto(mensajeResp.encode('utf-8'),address)
#           print(str(bytesTrasmitidos))
#           activado=True
#           break
      
#       if not activado:
#         mensajeResp = nroDisp + "#0##"
#         UDPServerSocket.sendto(mensajeResp.encode('utf-8'),address)  
      
#       activado=False
#       simDisp[5]=None #pongo en None ya que el usuario activo o no el dispositivo
      
#Primero inicio el servidor de Simuladores
# if(not st.session_state.servidorStart): #solo inicia una vez
#   hiloServidor = th.Thread(name='ServSimEntrenadorIoT' ,target=iniciarServidorSimulador, args=[st.session_state])
#   add_script_run_ctx(hiloServidor) #resuelve Thread missing ScriptRunContext
#   hiloServidor.start() #inicia servidor
#   st.session_state.servidorStart = True
#   print("Servidor de Simuladores Rutina iniciado")        
        
def leerRutinaExcel(uploaded, hoja):
    return pd.read_excel(io=uploaded, sheet_name=hoja)

def on_changeActivarSimulador(simDisp, activacion):
  print('OnChange CheckBox Simulador: ')
  print(simDisp)
  print('Activacion= ')
  print(activacion)
  if(simDisp==1):
    st.session_state.simDispositivo1[1]=activacion
    print(st.session_state.simDispositivo1)
  elif(simDisp==2):
    st.session_state.simDispositivo2[1]=activacion
    print(st.session_state.simDispositivo2)
  elif(simDisp==3):
    st.session_state.simDispositivo3[1]=activacion
    print(st.session_state.simDispositivo3)
  elif(simDisp==4):
    st.session_state.simDispositivo4[1]=activacion
    print(st.session_state.simDispositivo4) 
  elif(simDisp==5):
    st.session_state.simDispositivo5[1]=activacion
    print(st.session_state.simDispositivo5)
  elif(simDisp==6):
    st.session_state.simDispositivo6[1]=activacion
  elif(simDisp==7):
    st.session_state.simDispositivo7[1]=activacion      
  elif(simDisp==8):
    st.session_state.simDispositivo8[1]=activacion 
    
def on_clickRespSimDisp(simDisp, horaResp):
  #Aca debemos poner el tiempo en que el usuario hizo clic en el botn
  if(simDisp==1):
    st.session_state.simDispositivo1[4] = horaResp
    st.session_state.simDispositivo1[2]='Apagado'
  elif(simDisp==2):
    st.session_state.simDispositivo2[4] = horaResp
    st.session_state.simDispositivo2[2]='Apagado'
  elif(simDisp==3):
    st.session_state.simDispositivo3[4] = horaResp
    st.session_state.simDispositivo3[2]='Apagado'
  elif(simDisp==4):
    st.session_state.simDispositivo4[4] = horaResp
    st.session_state.simDispositivo4[2]='Apagado'
  elif(simDisp==5):
    st.session_state.simDispositivo5[4] = horaResp
    st.session_state.simDispositivo5[2]='Apagado'
  elif(simDisp==6):
    st.session_state.simDispositivo6[4] = horaResp
    st.session_state.simDispositivo6[2]='Apagado'
  elif(simDisp==7):
    st.session_state.simDispositivo7[4] = horaResp
    st.session_state.simDispositivo7[2]='Apagado'
  elif(simDisp==8):
    st.session_state.simDispositivo8[4] = horaResp
    st.session_state.simDispositivo8[2]='Apagado'
  
def on_startEjecutarRutina(d, pq, ti, tmr, resp, tiemposRespuesta):
  broadcast = '255.255.255.255'
  serverPort = 4022
  clientPort = 4023
  global reply
  global server

  print("Entra a ejecutar la rutina")
  print("Se duerme por (ms): "+str(ti))
  t.sleep(ti/1000) #Duermo el hilo hasta que llegue la hora de activacion del dispositivo. Ver Cambio de unidad ms a s
  timpoMaxRespuesta = tmr
  # Creo un socket para comunicacion por UDP
  
  print("Creo socket para envio de datos: "+ pq)
  clientSocket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM, sck.IPPROTO_UDP)   
  # Especifico opciones para el socket
  clientSocket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
  clientSocket.setsockopt(sck.SOL_SOCKET, sck.SO_BROADCAST, 1)
  clientSocket.bind((sck.gethostbyname(sck.gethostname()), clientPort))
    
  print('Solicita Respuesta: Si')
  clientSocket.settimeout((timpoMaxRespuesta/1000)+1) # tiempo maximo de espera respuesta 
    
  # Envio paquete respuesta UDP al servidor
  try:
    bytesTrasmitidos=clientSocket.sendto(pq.encode('utf-8'),(broadcast,serverPort)) 
        
    #  bytesTrasmitidos=clientSocket.sendto(pq.encode('utf-8'),(hostlocal,serverPort)) 
    print("Trama Enviada a dispositivo "+str(d)+ " - Trasmitidos " + str(bytesTrasmitidos) + " bytes")
    reply, server = clientSocket.recvfrom(64)
    strreply = reply.decode('utf-8') #Pasa byte array a String
    #se recibio respuesta del servidor
    print(strreply)
    pos_inic = strreply.index("#")+1
    pos_fin = strreply.index("##", pos_inic)
    
  
    tr = int(strreply[pos_inic:pos_fin])
    tiemposRespuesta.append(tr)
    print('Respuesta Servidor: {!r}'.format(reply))
    clientSocket.settimeout(None) #Luego de recibir la respuesta quito timeout
    if (reply is not None) and (server is not None):
      print('Recibido {!r} de {!s}'.format(reply, server))   
  
  except sck.timeout:
    # No se recibio respuesta del servidor
    if(resp):
      tiemposRespuesta.append(tmr+1)
      print(tiemposRespuesta)
      print("No se recibio respuesta del Dispositivo "+str(d))
    else:
      tiemposRespuesta.append(-1)
      print(tiemposRespuesta)

  finally:
    clientSocket.close()
    return 1 #Retorna 1 si no hubo error



st.set_page_config(layout="wide")

with open('./CSS/estilos.css') as formatos:
  cssContent = f'<style>{formatos.read()}</style>'

html_code = st.session_state.cssContent + '\n' + f'''<div class="bannerHeader">
                    <img src="data:image/png;base64,{st.session_state.imagen1}" width="400" height="120"/>
                    <img src="data:image/png;base64,{st.session_state.imagen2}" width="300" height="120"/>                   
                </div>'''

components.html(
    html_code, 
    height=140,
)





with st.container():
  styles_css = """
                <style>
                  button[role=tab]{
                    color: #FFF;
                    font-size: 26px !important;
                    color: #E74C3C;
                    padding: 0em 1em;
                    transition: all 0.3s;
                    position: relative;
                  }
                  button[role=tab]::before {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 1;
                    opacity: 0;
                    transition: all 0.3s;
                    border-top-width: 1px;
                    border-bottom-width: 1px;
                    border-top-style: solid;
                    border-bottom-style: solid;
                    border-top-color: rgba(255,255,255,0.5);
                    border-bottom-color: rgba(255,255,255,0.5);
                    transform: scale(0.1, 1);
                  }
                  button[role=tab]:hover p {
                    letter-spacing: 2px;
                  }
                  button[role=tab]:hover::before {
                    opacity: 1; 
                    transform: scale(1, 1); 
                  }
                  button[role=tab]::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 1;
                    transition: all 0.3s;
                    background-color: rgba(255,255,255,0.1);
                  }
                  button[role=tab]:hover::after {
                    opacity: 0; 
                    transform: scale(0.1, 1);
                  }
                  button[role="tab"] > div > p{
                    font-size: 26px !important;
                    color: #E74C3C;
                    padding: 0em 1em;
                  }
                  div[role="button"]{
                    font-size: 22px !important;
                    color: whitesmoke;
                    padding: 0em 1em;
                  }
                </style>
                
                """

  st.write(styles_css, unsafe_allow_html=True)
  tab1, tab2, tab3, tab4 = st.tabs(["Presentación", "Prototipo", "Aplicación Web", "Programa de Estudio"])
  html_code = st.session_state.cssContent + '\n' + f'''<div style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap; gap:10px; justify-content: space-between; background-color: black; padding-right: 10px; min-width: 800px;">
                    <img src="data:image/png;base64,{st.session_state.imagen3}" width="120" height="40" style="margin-left: 10px;"/>
                    <p style="font-size:14; font-weight:bold; color: orange;"> Ing. Sebastián Rocco - UTN FRSF - EETP Nº 479 Manuel D. Pizarro - EETP Nº 480 Manuel Belgrano - Santa Fe - Argentina</p>                   
                </div>'''  
  components.html(
    html_code, 
    height=100,
  )             
with tab1:
    screen_width = 1366
    emptycolumnprop = ((screen_width-400)/2)/400
    
    emptyLeft, colVideo, emptyRight = st.columns([0.5,1,0.5])
    with emptyLeft:
        st.markdown('<h2 style="color: orange; text-align: center;">Proyecto Entrenador IoT</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: justify; color: whitesmoke; font-size: 1.2em;">Aplicaremos el Internet de las Cosas implementando un <span style="color:yellow; font-weight: bold;">prototipo</span> de dispositivo diseñado para entrenar el cuerpo y el cerebro, mejorando el tiempo de reacción, la precisión mental, el procesamiento sensorial y otros atributos neurocognitivos. </p>', unsafe_allow_html=True)
    
    with colVideo:
        st.markdown('<h2 style="color: orange; text-align: center;">¿Como trabajan estos entrenadores?</h2>', unsafe_allow_html=True)
        # video_file = open('./videoFitLight.mp4', 'rb') #enter the filename with filepath

        # video_bytes = video_file.read() #reading the file

        # st.video(video_bytes) #displaying the video
        st.video("https://youtu.be/krqhHoWKhj4")
    
    with emptyRight:
        st.markdown('<h2 style="color: orange; text-align: center;">Objetivos del Taller</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: justify; color: whitesmoke; font-size: 1.2em;">Proporcionar a los alumnos <span style="color: yellow; font-weight: bold;">conocimientos teóricos, herramientas, prácticas, métodos y técnicas </span> que se articulen en trabajos multidisciplinarios en el campo de la electrónica, Software y Hardware libre, los microcontroladores, el Internet de las Cosas y la Programación. </p>', unsafe_allow_html=True)
        
with tab2:
    with st.expander('Prototipo Entrenador IoT - Elementos para el montaje'):
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image("./Images/protoboard.png")
                st.markdown("<h3>Protoboard 830 - Cantidad: 1 </h3>", unsafe_allow_html=True)
            with col2:
                st.image("./Images/fuente protoboard.png")
                st.markdown("<h3>Fuente para Protoboard 3.3V 5V Usb mini - Cantidad: 1 </h3>", unsafe_allow_html=True)
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image("./Images/wemos.png")
                st.markdown("<h3>Wemos D1 Mini - Cantidad: 1 </h3>", unsafe_allow_html=True)
            with col2:
                st.image("./Images/led RGB.png")
                st.markdown("<h3>Circulo 3 Leds Rgb 5050 Ws2812 Neopixel - Cantidad: 1 </h3>", unsafe_allow_html=True)
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image("./Images/buzzer.png")
                st.markdown("<h3>Módulo Zumbador Pasivo 3.3V 5V 3.1KHZ 80DB - Cantidad: 1 </h3>", unsafe_allow_html=True)
            with col2:
                st.image("./Images/HCSR04.png")
                st.markdown("<h3>Módulo Sensor Ultrasónico de distancia HC-SR04 - Cantidad: 1 </h3>", unsafe_allow_html=True)        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image("./Images/cables.png")
                st.markdown("<h3>Jumper Pack Dupont Macho-Macho 20cm y 10cm - Cantidad: necesaria </h3>", unsafe_allow_html=True) 
            with col2:
                st.image("./Images/usbaminiusb.png")
                st.markdown("<h3>Cable USB a Mini USB - Cantidad: 1 </h3>", unsafe_allow_html=True) 
               
    with st.expander('Esquema de Montaje: Entrenador IoT'):
      with st.container():
        st.markdown('<h2 style="color: orange; text-align: right;">Diseño Preliminar con Arduino I y ESP8266</h2>', unsafe_allow_html=True)
        st.image("./Images/disenoPreliminar.png", width=800)
      with st.container():
        st.markdown('<h2 style="color: orange; text-align: right;">Diseño Mejorado con Wemos D1 Mini</h2>', unsafe_allow_html=True)
        st.image("./Images/montaje.png", width=800)
    with st.expander('Código Entrenador IoT'):
        with st.container():
            codigo = '''#include <Adafruit_NeoPixel.h> 
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Adafruit_NeoPixel.h es una librería para controlar pixeles LED de un solo cable WS2812.</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: justify'> ESP8266WiFi.h es una librería para configurar la red de un ESP8266.</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: justify'> WiFiUdp.h es una librería para implementar una comunicación UDP en el ESP8266.</p>", unsafe_allow_html=True)            
        
        with st.container():
            codigo = '''const int TRIGGERPIN = 13;
const int ECHOPIN = 14;
const int BUZZER = 5;
const int LED = 4;
const int NUMLEDS = 3;
const int TAMMAXPAQUDP = 255;
const int DISPOSITIVO = 1;
const unsigned int UDP_PORT = 4022;
#define WIFI_SSID "XXXXXXXXXX"
#define WIFI_PASSW "XXXXXXXXXX"'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Definimos constantes para determinar los pines en el Wemos D1 Mini: 13 y 14 para el HC SR04, 5 para el Buzzer pasivo, 4 para el Led RGB. Además definiremos que el Dispositivo se identificará como 1, se define un tamaño maximo de paquete UDP en 255 bytes, el puerto UDP en 4022. Por último se establece el SSID y la contraseña de seguridad de la red WiFi a la cual se conectará el dispositivo Entrenador IoT</p>", unsafe_allow_html=True)
        
        with st.container():
            codigo= '''int tamañoPaquete = 0;
bool errorConexion = false;
char paqueteUDP[TAMMAXPAQUDP];
int dataMaxT = 0;
int dataCRojo = 0;
int dataCVerde = 0;
int dataCAzul = 0;
int dataTono = 0;
int dataDistCM = 0;
bool dataRespuesta = false;
long tactivacion = 0;

Adafruit_NeoPixel pixels(NUMLEDS, LED, NEO_GRB + NEO_KHZ800);
WiFiUDP UDP;'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Posteriormente declaramos un conjunto de variables para administrar los paquetes UDP (protocolo de aplicación). Las dos últimas líneas instacian los objetos de las librerías para controlar el LED y la comunicación UDP.</p>", unsafe_allow_html=True)   

        with st.container():
            codigo= '''int activar(int maxT, int cRojo, int cVerde, int cAzul, int tono, int maxDistCM){
  //Prendemos el LED o los LEDS
  unsigned long tiempo = millis();
  bool activacion = false;
  Serial.println("Entro a la funcion de activacion del dispositivo");
  for(int i=0; i<NUMLEDS; i++){
    pixels.setPixelColor(i, pixels.Color(cRojo, cVerde, cAzul));
  }
  pixels.show();

  //Activamos Buzzer
  tone(BUZZER,tono); //digitalWrite(LOW); si es buzzer activo low level trigger

  //Calibramos sensor distancia
  long echoTiempo;
  long distCM;
  long tiempoActivacion;

  //Verificamos proximidad
  while (tiempo+maxT > millis()){
    digitalWrite(TRIGGERPIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGERPIN, LOW);
    echoTiempo= pulseIn(ECHOPIN, HIGH);
    distCM = echoTiempo/59;
    if(distCM <= maxDistCM){
      activacion=true;
      tiempoActivacion = millis()-tiempo; //Guarda la cantidad de milisegundos que tardo en activar
      //Ahora apagar LED
      pixels.clear();
      pixels.show();
      noTone(BUZZER); //digitalWrite(HIGH); si es buzzer activo low level trigger
    }
  }
  if(activacion) return tiempoActivacion;
  else return 0;
}'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Declaración e implementación de una función para la activación del dispositivo. Es invocada luego de que llega el paquete UDP y se verifica que el número de dispositivo al cual esta enviado el paquete coincide con el número de dispositivo definido en la sección de constantes. En caso contrario se descarta el paquete y esta función no será invocada.</p>", unsafe_allow_html=True)   
            st.markdown("<p style='text-align: justify'> Veamos la línea distCM = echoTiempo/59 -> Partiremos de la siguiente fórmula:</p>", unsafe_allow_html=True)
            st.latex(r'''Velocidad = \frac{distancia recorrida}{tiempo}''') 
            st.markdown("<p style='text-align: justify'> Donde la <b>Velocidad</b> es la velocidad del sonido 340m/s, pero usaremos las medidas en cm/us pues trabajaremos en centímietros y microsegundos, <b>tiempo</b> es el tiempo que demora en llegar el ultrasonido al objeto y regresar al sensor, y la <b>distancia recorrida</b> es dos veces la distancia hacia el objeto. Reemplazando las fórmulas obtenemos:</p>", unsafe_allow_html=True)
            st.latex(r'''\frac{340}{s}\centerdot\frac{1s}{1000000us}\centerdot\frac{100cm}{1m}\centerdot = \frac{2d}{t} \therefore d(cm) = \frac{t(us)}{59}''')            
            
        with st.container():
            codigo= '''int procesarPaqueteUDP(){
  String spudp = String(paqueteUDP);
  int lastIndex = 0;
  int index = spudp.indexOf('#',0);
  if(index<0) return -1;
  String token = spudp.substring(lastIndex,index);
  Serial.print("DISPOSITIVO: ");
  Serial.println(token);
  if(DISPOSITIVO!=token.toInt()) return 0;
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Tiempo Max Encendido: ");
  Serial.println(token);
  dataMaxT = token.toInt(); //Obtiene la cantidad maxima de tiempo a esperar del dispositivo
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Rojo: ");
  Serial.println(token);
  dataCRojo = token.toInt(); //Obtiene nivel saturacion color Rojo
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Verde: ");
  Serial.println(token); 
  dataCVerde = token.toInt();  //Obtiene nivel saturacion color Verde
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Azul: ");
  Serial.println(token);
  dataCAzul = token.toInt(); //Obtiene nivel saturacion color Azul 
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Tono: ");
  Serial.println(token);
  dataTono = token.toInt(); //Obtiene frecuencia activacion Buzzer pasivo
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Distancia Max CM: ");
  Serial.println(token);
  dataDistCM = token.toInt(); //Obtiene distancia en CM sensor de proximidad
  lastIndex = index;
  index = spudp.indexOf('#',index+1);
  if(index<0) return -1;
  token = spudp.substring(lastIndex+1,index);
  Serial.print("Solicita Respuesta: ");
  Serial.println(token);
  if (token.toInt()>0) dataRespuesta =true; //Obtiene si el cliente solicita respuesta o no
  else dataRespuesta=false;
  return 1;   
}'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Declaración e implementación de una función para parsear el contenido del paquete UDP que llega al dispositivo para su procesamiento.</p>", unsafe_allow_html=True)   

        with st.container():
            codigo='''void setup() {
  // put your setup code here, to run once:
  pinMode(LED, OUTPUT);  
  pinMode(TRIGGERPIN, OUTPUT);
  pinMode(ECHOPIN,INPUT);
  
  Serial.begin(9600);
  Serial.println("Configuro los pines");
  pixels.begin();
  Serial.println("Inicializa objeto NeoPixels Adafruit");
  //Inicializa WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID,WIFI_PASSW);
  Serial.println("Inicializa WiFi con SSI y PASSW");
  //Conecta a la red por WiFi
  int intentosConexion = 1;
  Serial.println("Inicia proceso de intentos de conexion");
  while ((WiFi.status() != WL_CONNECTED) && (intentosConexion<100)){ //intenta por 25 segundos
    if(intentosConexion%2 > 0){
      //Enciendo la luz blanca
      for(int i=0; i<NUMLEDS; i++){
        pixels.setPixelColor(i, pixels.Color(255, 255, 255));
      }
      Serial.print('.');
      pixels.show();
    }else{ //apaga los Leds
      pixels.clear();
      pixels.show();
    }
    //Incrementa intentosConexion en 1
    intentosConexion++;
    delay(500);
  }
  //WiFi conectado o error de Conexion
  if(intentosConexion<100){
    //Se pudo conectar
    pixels.clear();
    pixels.show();
    Serial.println();
    Serial.println("Conectado a la red");
    UDP.begin(UDP_PORT); //Se pone a escuchar en el puerto UDP
    Serial.println("Escucha en puerto 4022");
  }else{
    //No se pudo conectar - Deja luz blanca encendida como error de conexion 
    Serial.println("Fallo de conexion WiFi");
    for(int i=0; i<NUMLEDS; i++){
      pixels.setPixelColor(i, pixels.Color(255, 255, 255));
    }
    pixels.show();
    errorConexion = true;
  }
}'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Implementación de la función setup de Arduino utilizada para la inicialización de variables, objetos... antes de proceder con la función loop.</p>", unsafe_allow_html=True)   

        with st.container():
            codigo= '''void loop() {
  
  if(!errorConexion){  
    //Recepción de paquete UDP
    tamañoPaquete =  UDP.parsePacket();
    if(tamañoPaquete){
      Serial.println("Recibe paquete UDP");
      //Se recibió un paquete
      UDP.read(paqueteUDP,TAMMAXPAQUDP);
      Serial.println("Paquete: ");
      Serial.println(paqueteUDP);
      //Se procesa el paquete para obtener los campos
      if(procesarPaqueteUDP()>0){
        Serial.println("Proceso el Paquete");
        //El procesamiento tuvo exito, se obtuvieron los campos
        tactivacion = activar(dataMaxT, dataCRojo, dataCVerde, dataCAzul, dataTono, dataDistCM);
        if(tactivacion>0){
          //El usuario activo el dispositivo
          if(dataRespuesta>0){
            //Enviar respuesta al cliente
            UDP.beginPacket(UDP.remoteIP(),UDP.remotePort());
            UDP.print((String)DISPOSITIVO);
            UDP.print("#");
            UDP.print((String)tactivacion);
            UDP.print("##");
            //UDP.print(...)  //Esto dice en caso de usar ESP32
            UDP.endPacket(); 
          } //Sino se solicita respuesta no hace nada
        }else{
          //No se pudo activar el dispositivo en el tiempo maximo
          if(dataRespuesta>0){
            //Enviar respuesta al clliente
            UDP.beginPacket(UDP.remoteIP(),UDP.remotePort());
            UDP.print((String)DISPOSITIVO);
            UDP.print("#");
            UDP.print("0");
            UDP.print("##");
            //UDP.print(...)  //Esto dice en caso de usar ESP32
            UDP.endPacket(); 
          } //Sino se solicita respuesta no hace nada
        }
        pixels.clear(); //Apagamos los Leds
        pixels.show();      
        noTone(BUZZER); //digitalWrite(BUZZER,HIGH); si el Buzzer Activo Low Level Trigger
      }else{
        Serial.println("Error en el procesamiento del paquete");
      }
    }
  }
}'''
            st.code(codigo, language='c')
            st.markdown("<p style='text-align: justify'> Implementación de la función loop de Arduino que se ejecutará hasta que se resetee el microcontrolador Wemos D1 Mini o se corte su suministro de energía.</p>", unsafe_allow_html=True)   
    with st.expander('Prueba de Funcionamiento del Dispositivo - Entrenador IoT'):
        with st.container():
          st.markdown('<h2 style="color: orange; text-align: center;">Probando el prototipo y el sketch del Entrenador IoT</h2>', unsafe_allow_html=True)
          # video_file = open('./presentacionEntrenadorIoT_480p.mp4', 'rb') #path relativo archivo .mp4
          # video_bytes = video_file.read() #como es un video local lo leemos
          # st.video(video_bytes) #Visualizamos el video con el componente st.video 
          st.video("https://youtu.be/FPbXWjT3c8A")
with tab3:      
  with st.container():
    st.markdown(f"<h3>App Rutinas de Entrenamiento</h3>", unsafe_allow_html=True)
    uploadedFile = st.file_uploader("Cargar Archivo",type=['xlsx'])   
    if uploadedFile is None:
      st.warning("Seleccione un archivo excel (*.xlsx) que contenga la rutina a ejecutar")      
    
    with st.form("form_Rutina"):
      hoja = st.text_input("Nombre de la Hoja con la Rutina", help="Ingrese el nombre de la hoja en el archivo excel que tiene la rutina a ejecutar", placeholder="Nombre de la Hoja Excel que contiene la rutina")
      submitted = st.form_submit_button("Submit")
      if submitted:
        st.session_state.rutinaDatos = leerRutinaExcel(uploadedFile, hoja)
        st.write(st.session_state.rutinaDatos)
        st.session_state.rutinaCargada = True
        st.session_state.rutinaEjecutada = False
      
    if (st.session_state.rutinaCargada and not st.session_state.rutinaEjecutada):
      tiempoTotalRutina = 0
      clikedEjecutar = st.button("Ejecutar Rutina",disabled=False)
      if(clikedEjecutar) is True:
        dataframe = st.session_state.rutinaDatos

        #Recorrer dataframe uno a uno y enviar los datagrama UDP
        st.session_state.tiemposRespuesta.clear()
        progreso = st.progress(0)
        
        for i in range(len(dataframe)):
          # Convierto tokens protocolo aplicacion entrenador IoT a los tipos de las variables
          # esperados por la función on_clickedEjecutarRutina(...)
          tiempoInicio=dataframe.iloc[i]['TiempoAccion']
          tiempoMax=dataframe.iloc[i]['TiempoMaxAct']
          esperaRespuesta = (dataframe.iloc[i]['Respuesta']>0)
          
          hiloRutina = th.Thread(target=on_startEjecutarRutina, args=[dataframe.iloc[i]['Dispositivo'], dataframe.iloc[i]['Paquete'], tiempoInicio, tiempoMax, esperaRespuesta, st.session_state.tiemposRespuesta])
          hiloRutina.start() #Inicia schedule activacion Dispositivo
          tiempoTotalRutina = tiempoInicio + tiempoMax
        
        print(tiempoTotalRutina) #muestro tiempo total de la rutina

      
        for p in range(11):
          t.sleep((tiempoTotalRutina/10)/1000)
          progreso.progress(p/10)  
        st.session_state.rutinaEjecutada = True
      
      if(st.session_state.rutinaCargada and st.session_state.rutinaEjecutada):
        st.session_state.rutinaDatos['Tiempo Respuesta']=st.session_state.tiemposRespuesta

        x = np.arange(1,len(st.session_state.rutinaDatos["TiempoAccion"])+1,1)
        ancho = 0.35 #ancho de las barras
        plt.rcParams.update({
          "lines.color": "white",
          "patch.edgecolor": "white",
          "text.color": "white",
          "axes.facecolor": "#404040",
          "axes.edgecolor": "lightgray",
          "axes.labelcolor": "white",
          "xtick.color": "white",
          "ytick.color": "white",
          "grid.color": "lightgray",
          "figure.facecolor": "black",
          "figure.edgecolor": "black",
          "savefig.facecolor": "black",
          "savefig.edgecolor": "black"})
        grafica, ax = plt.subplots()
        #tiempo Activacion
        barras1 = ax.bar( x - ancho/2, st.session_state.rutinaDatos["TiempoMaxAct"], width=ancho, color="#f7c707", label="Tiempo Maximo Respuesta")
        barras2 = ax.bar( x + ancho/2, st.session_state.rutinaDatos["Tiempo Respuesta"], width=ancho, color="#006666", label="Tiempo Respuesta Usuario")

        ax.set_title("Tiempos de respuesta a las activaciones de los dispositivos de entrenamiento")
        ax.set_xlabel("Milisegundos")
        ax.set_ylabel("Milisegundos")
        ax.set_xticks(x, st.session_state.rutinaDatos["TiempoAccion"])
        
        ax.legend()
        ax.bar_label(barras1, padding=3)
        ax.bar_label(barras2, padding=3)
        grafica.tight_layout()
        grafica       
        st.session_state.rutinaEjecutada = False
        
        
        
 
with tab4:
  progTaller = '''  
## Programa Taller:
### Total Horas Cátedra Semanales: 5
### Dictado: Anual
 
## Destinatarios: 
Alumnos del segundo ciclo de la Educación Técnica Profesional. 
  - Terminalidad Informática Personal y Profesional: **Taller - 4to año**.
  - Terminalidad Equipos e Instalaciones Electromecánicas: **Electrónica – 5to año**.

## Unidades 
### 1. Arduino: Introducción 
*	Microcontroladores y microprocesadores.
*	Interfaces Analógico – Digital: DAC, ADC.
*	Modelos de Arduino: UNO, MEGA, PRO MINI, MICRO, NANO…
*	Hardware: Arduino(PINOUT), Shields, Sensores, Actuadores, periféricos, Entradas analógicas y digitales …
*	Instalación de IDE (Entorno de Desarrollo Integrado) Arduino.
*	Instalación de drivers (CH340)
  Tiempo aproximado duración: 1 mes (4 clases)

### 2. Arduino: Lenguaje.
*	Boceto (sketch): bloques setup(), loop().
*	Nociones básicas del lenguaje C++.
*	Análisis de código (sketch)
*	Carga del boceto a Arduino, compilación y subida del sketch (bootloader).
*	Funciones básicas: pinMode, delay, digitalWrite, DigitalRead, analogRead…
*	Pines PWM y analogWrite.
  Tiempo aproximado duración: 1 mes (4 clases)

### 3. Arduino: Prácticas
*	Montaje de Circuitos e implementación de sketchs.
  +	Prácticas con Leds (Blink, RGB).
  +	Monitor Serial (Serial Object). Comunicar Arduino con la PC, Debugging)
  +	Sensores: fotoresistencias, sensor de humedad y temperatura, ultrasonido, infrarrojo, detección de gases…
  +	Interruptores (resistencias Pull Up y Pull Down), codificadores
  +	Transistores, optoacopladores, relé.
  +	Motores de Corriente Continua, drivers L298N…
  +	Motores Paso a Paso, drivers A4988, driver DRV8825
  +	Displays, pantallas.
  +	Comunicación por bus SPI, ISP, I2C
  +	Comunicación Bluethoot
  +	ESP8266 – Wemos D1 Mini – Nodemcu para Comunicación WiFi (TCP-UDP)
  +	Domótica - Zigbee
  Tiempo aproximado duración: 5 meses (20 clases)
'''
  st.markdown(progTaller)


