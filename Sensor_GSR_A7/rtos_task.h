#pragma once
#include <Arduino.h>
//#include <cstddef>
//#include <cstdint>
//#include "globals.h"
//#include <imu_header.h>
//
// FreeRTOS task declarations and helpers for the peripheral foot firmware.
/// VAR///
//extern timer_0;


// Handlers
//TaskHandle_t Task_LED_Handle 				= NULL; 
//TaskHandle_t Task_FSRRead_Handle 		= NULL;
TaskHandle_t Task_GSRRead_Handle 		= NULL;
//TaskHandle_t Task_SerialShow_Handle 	= NULL;
TaskHandle_t Task_BLE_Handle 				= NULL;
//TaskHandle_t Task_Monitor_Handle		 	= NULL;
//TaskHandle_t Task_QueueMonitor_Handle	= NULL;
//TaskHandle_t Task_TimeKeeper_Handle	= NULL;
//TaskHandle_t Task_LocalTimerWacher_Handle	= NULL;

// Queues
QueueHandle_t GSR_fifo= NULL; // fifo for the FSR data
//QueueHandle_t t0Queue; // Fifo for the change of time


// defines
#define FIFO_SIZE 5000
#define T0_FIFO_SIZE 16
// usefull funtions
//
// LED(uint8_t r, uint8_t g, uint8_t b)

//xTaskCreate(
//  tareaFuncion,      // Función de la tarea
//  "NombreTarea",     // Nombre identificador
//  1000,              // Tamaño de la pila
//  NULL,              // Parámetro (puedes pasar datos)
//  1,                 // Prioridad
//  NULL               // Handle (opcional, para referenciar luego)
//);

//xQueueCreate()	Crea una cola con un tamaño y tipo de dato fijo
//xQueueSend()	Envia un dato a la cola (desde una tarea o ISR)
//xQueueReceive()	Recibe un dato de la cola (bloquea hasta que haya datos si querés)
//xQueuePeek()	Mira el dato sin sacarlo de la cola
//void TaskLEDTest(void *pvParameters);
void TaskGSRRead(void*pvParameters);
//void TaskSerialShow(void *pvParameters);
void TaskBLE(void *pvParameters);
//void TaskMonitor(void *pvParameters);
//void TaskQueueMonitor(void *pvParameters);
//void printFSRData(FSR_data_t &data);
//static void TaskTimeKeeper(void* pvParameters);
//void printFSRData_2(FSR_data_t &data);
//void TaskLocalTimerWatcher(void *pvParameters);
void printGSRData(GSR_data_t *data);

// Create queues, attach interrupts and spawn all FreeRTOS tasks.
void init_freertos_tasks()
{ 
  	
	/////////////////////////////////fifo decla///////
	GSR_fifo = xQueueCreate(FIFO_SIZE,sizeof(GSR_data_t));
	if(GSR_fifo==NULL)
	{Serial.print("error creating queue 1"); while(1);}
	
	//xTaskCreatePinnedToCore(TaskLocalTimerWatcher,"LocalTimerwatcher",4096,NULL,13,&Task_LocalTimerWacher_Handle,1);
	
	//xTaskCreate(TaskLEDTest,"TaskLEDTest",4000,NULL,2,&Task_LED_Handle);
	xTaskCreate(TaskGSRRead,"TaskGSRRead",10096,NULL,10,&Task_GSRRead_Handle);
	xTaskCreate(TaskBLE,"TaskBLE",10096,NULL,20,&Task_BLE_Handle);

                //task monitor
   //xTaskCreatePinnedToCore(TaskMonitor, "TaskMonitor", 2548, NULL, 1, &Task_Monitor_Handle,1);
   //xTaskCreatePinnedToCore(TaskQueueMonitor, "QueueMonitor", 2548, NULL, 1, &Task_QueueMonitor_Handle,1);


		//vTaskSuspendAll();
		//vTaskResume(&Task_TimeKeeper_Handle);

}



//////////////////////////////Task declaration/////////////////////////////
// Read FSR sensors and push samples into the queue.
void TaskGSRRead(void *pvParameters)
{
   GSR_data_t data_GSR;
	GSR_data_t data_to_print;
	//int64_t t_temp;
	//int64_t get_local_time_us()

	while (true) 
	{
		data_GSR.time_stamp =esp_timer_get_time();
	
		data_GSR.GSR =analogRead(analogPin); 

		// int fsr0 = (analogRead(A4) > 1800) ? 1 : 0;
  //int fsr1 = (analogRead(A5) > 1400) ? 1 : 0;
  //int fsr2 = (analogRead(A6) > 1200) ? 1 : 0;
  //int fsr3 = (analogRead(A7) > 1600) ? 1 : 0;

	
		if(xQueueSend(GSR_fifo,&data_GSR,portMAX_DELAY)==pdPASS)
		{//Serial.println("data added to FIFO ");
		 	data_to_print=data_GSR;
			printGSRData(&data_to_print);
		}
		else{
			//Serial.println("FIFO FULL");
		}	
		//vTaskDelay(pdMS_TO_TICKS(int(1000/FSR_SAMPLE_RATE)));
		vTaskDelay(pdMS_TO_TICKS(100));
	}
}
///////////////////// TaskBLE//////////////////////
// Handles BLE connections and transmits queued FSR data.
// Es recomendable que el stack ocupado por el BLE este inicializado antes de
// su uso, por ende, ojala iniciarlo en el setup o antes del bucle principal
// de la TASK

void TaskBLE(void *pvParameters)
{ 
   GSR_data_t data_GSR;
	char buffer[sizeof(GSR_data_t)+40];

	vTaskSuspend(Task_GSRRead_Handle);
	while (true) 
	{
  	 	//BLEDevice central = BLE.central();
  		//rainbow(); // rainbow led till the Bluetooth is connected

  		if(NimBLEDevice::getServer()->getConnectedCount())
  		{
				
  		  Serial.println("Connected to central device");
  		  Serial.print("Device MAC address: ");
  		  //Serial.println(central.address());	    
		  vTaskResume(Task_GSRRead_Handle);
		  //LED(1u,1u,1u);// device connected and sending data 
  			while (NimBLEDevice::getServer()->getConnectedCount()) // Mientras siga conectado
      	{
        		if (xQueueReceive(GSR_fifo, &data_GSR, portMAX_DELAY) == pdPASS)
        		{
          		GSRDataToCSV_char(&data_GSR, buffer, sizeof(buffer));

          		// Enviar por BLE
          		pSensorCharacteristic->setValue((uint8_t*)buffer, strlen(buffer));
          		pSensorCharacteristic->notify(); // Notifica el valor actual
        		}
				else
				{
					vTaskDelay(pdMS_TO_TICKS(20));
				}
      	}
  		  //LED(0,0,0);
		  // Re advertising if get disconected
		  Serial.print("Client disconected");
		  NimBLEDevice::startAdvertising();
  		
  		}
		else {vTaskDelay(pdMS_TO_TICKS(10));}

	}
}

void printGSRData(GSR_data_t *data_GSR)
{
	Serial.print(data_GSR->time_stamp);
	Serial.print(",");
	Serial.println(data_GSR->GSR);

}
//funtions/////////
//
// Debug print of first four FSR values.

