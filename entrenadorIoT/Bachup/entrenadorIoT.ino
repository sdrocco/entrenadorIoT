#include <Adafruit_NeoPixel.h> 
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const int TRIGGERPIN = 13;
const int ECHOPIN = 14;
const int BUZZER = 5;
const int LED = 4;
const int NUMLEDS = 3;
const int TAMMAXPAQUDP = 255;
const int DISPOSITIVO = 1;
const unsigned int UDP_PORT = 4022;
#define WIFI_SSID "FAMILIA CARDOZO"
#define WIFI_PASSW "colon1492"

int tamañoPaquete = 0;
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
WiFiUDP UDP;

int activar(int maxT, int cRojo, int cVerde, int cAzul, int tono, int maxDistCM){
  //Prendemos el LED o los LEDS
  unsigned long tiempo = millis();
  bool activacion = false;
  Serial.println("Entro a la funcion de activacion del dispositivo");
  pixels.clear();
  for(int i=0; i<NUMLEDS; i++){
    pixels.setPixelColor(i, pixels.Color(cRojo, cVerde, cAzul));
  }
  pixels.show();

  //Activamos Buzzer
  tone(BUZZER,tono,maxT);

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
      noTone(BUZZER);
    }
  }
  if(activacion) return tiempoActivacion;
  else return 0;
}


int procesarPaqueteUDP(){
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
}

void setup() {
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
        Serial.print('.');
      }
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
}


void loop() {
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
    }else{
      Serial.println("Error en el procesamiento del paquete");
    }
  }
}
