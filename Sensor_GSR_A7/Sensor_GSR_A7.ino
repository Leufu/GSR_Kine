int analogPin = A7;     
int data = 0;           

void setup(){

  Serial.begin(9600);            //  setup serial

}

void loop(){
  
    data = analogRead(analogPin);    // read the input pin
    Serial.println(data);   

} // Void Loop
