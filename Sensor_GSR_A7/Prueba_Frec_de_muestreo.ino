const int GSR = A7;
int numeroMuestras = 1000;  // Reducir el número de muestras para evitar que el tiempo total sea muy corto
int Serial_speed = 9600;

void setup() {
  Serial.begin(Serial_speed);
  Serial.println("Tiempo promedio en us para tomar lecturas analogRead():");
}

void loop() {
  unsigned long time0 = micros();
  for (int i = 0; i < numeroMuestras; i++) {
    analogRead(GSR);
  }
  unsigned long timen = micros() - time0;

  float promTimeMuestras = (float)timen / numeroMuestras;  // Promedio en microsegundos por lectura

  Serial.print(promTimeMuestras);
  Serial.println(" us per analogRead");

  delay(1000);  // Esperar 1 segundo antes de la próxima medición
}

//codigo demuestra que el sample rate 112 us
// es decir toma 8929 muestras en un segundo
