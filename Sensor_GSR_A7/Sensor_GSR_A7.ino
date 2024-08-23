int analogPin = A7;     
int dataRaw=0;
int data = 0;           
long sum=0;

void setup(){

  Serial.begin(9600);            //  setup serial

}
void loop(){
//unsigned long startTime = millis(); // Registra el tiempo de inicio
    long sum = 0;
    for(int i=0;i<=100;i++){
     dataRaw = analogRead(analogPin);    // read the input pin 
       sum += dataRaw;
      delay(1);
    }
   data = sum/100;
//   Serial.print("Data: ");
   Serial.println(data);   
//   unsigned long endTime = millis(); // Registra el tiempo de fin
//   long elapsedTime = endTime - startTime; // Calcula el tiempo transcurrido
//   Serial.print("Elapsed time (ms): ");
//   Serial.println(elapsedTime);
} // Void Loop
