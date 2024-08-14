const int GSR=A7;
int sensorValue=0;
int gsr_average=0;
int Serial_speed=115200; 
int promedio_variable=10;

void setup(){
  Serial.begin(Serial_speed);
}

void loop(){
  long sum=0;
  for(int i=0;i<promedio_variable;i++)           //Average the 10 measurements to remove the glitch
      {
      sensorValue=analogRead(GSR);
      sum += sensorValue;
      delay(5);
      }
   gsr_average = sum/10;
   Serial.println(gsr_average);
}
