const int GSR=A7;
int sensorValue=0;

unsigned long lastTime = 0;
unsigned long currentTime = 0;
float samplingFrequency = 0;

int Serial_speed=9600; 

//simplificación del código para comprobar la frecuencia de muestreo

#include "utilidades.h"
void setup(){
  Serial.begin(Serial_speed);
}

void loop(){
  currentTime = micros();  // Tiempo actual en microsegundos

  sensorValue = analogRead(A7);
  Serial.print("Valor sensor: ");
  Serial.print(sensorValue);
  Serial.println(" ");

 
//Revisar las variables

  unsigned long dt = currentTime - lastTime;  // Tiempo entre lecturas
  samplingFrequency = 1000000 / dt;  // Frecuencia de muestreo en Hz

  Serial.print("Frecuencia de muestreo: ");
  Serial.print(samplingFrequency);
  Serial.println("Hz");

  lastTime = currentTime;  // Actualizar el tiempo para la siguiente iteración
}
