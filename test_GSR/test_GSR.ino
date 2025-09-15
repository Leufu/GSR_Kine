#define analogPin A10  
int dataRaw=0;
int data_sum = 0;           
long sum=0;

void setup(){

  Serial.begin(115200);            //  setup serial
  while (!Serial);
  Serial.println("trying");
}
void loop(){
//unsigned long startTime = millis(); // Registra el tiempo de inicio
    long sum = 0;
    for(int i=0;i<=100;i++){
     dataRaw = analogRead(analogPin);    // read the input pin 
       sum += dataRaw;
      delay(1);
    }
   data_sum = sum/100;
//   Serial.print("Data: ");
   Serial.println(data_sum);   
   //delay(100);
//   unsigned long endTime = millis(); // Registra el tiempo de fin
//   long elapsedTime = endTime - startTime; // Calcula el tiempo transcurrido
//   Serial.print("Elapsed time (ms): ");
//   Serial.println(elapsedTime);
} // Void Loop
