///////// Var tiempo////////////
unsigned long startTime;
unsigned long elapsedTime;

void Time_Start_Task(){startTime = micros();}
void Time_Finish_Task(const String &Name_function )
{
  unsigned long endTime = micros(); // End time of the function
  elapsedTime = endTime - startTime; // Calculate elapsed time
  Serial.print("La funcion "); Serial.print(Name_function); Serial.print(":"); 
  Serial.print("Elapsed time (microseconds): ");
  Serial.println(elapsedTime); // Print the elapsed time
}

void Halt_Task(){Serial.print("PROGRAMA DETENIDO");while(1);}
