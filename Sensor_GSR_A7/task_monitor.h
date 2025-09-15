#pragma once

// Utilities to monitor FreeRTOS tasks and queues.
// ========= ESTRUCTURAS DE MONITOREO =========
////#//include "task.h"
// Basic information about a task to be monitored.
struct MonitoredTask {
        const char* name;
        TaskHandle_t* handle;
};

// Basic information about a queue to be monitored.
struct MonitoredQueue {
        const char* name;
        QueueHandle_t* handle;
};

//void TaskLEDTest(void *pvParameters);
//void TaskFSRRead(void*pvParameters);
//void TaskSerialShow(void *pvParameters);
//void TaskBLE(void *pvParameters);
//void TaskMonitor(void *pvParameters);
//void TaskQueueMonitor(void *pvParameters);
//void printFSRData(FSR_data_t &data);
//static void TaskTimeKeeper(void* pvParameters);
//void printFSRData_2(FSR_data_t &data);
//void TaskLocalTimerWatcher(void *pvParameters);
//TaskHandle_t Task_LED_Handle 				= NULL; 
//TaskHandle_t Task_FSRRead_Handle 		= NULL;
//TaskHandle_t Task_SerialShow_Handle 	= NULL;
//TaskHandle_t Task_BLE_Handle 				= NULL;
//TaskHandle_t Task_Monitor_Handle		 	= NULL;
//TaskHandle_t Task_QueueMonitor_Handle	= NULL;
//TaskHandle_t Task_TimeKeeper_Handle	= NULL;
//TaskHandle_t Task_LocalTimerWacher_Handle	= NULL;



//#include <freeRtos.h>
////////////////////////////////
// added Tasks for task monitor
//
// ================== CONFIG ==================
unsigned int MONITOR_TASK_DELAY_MS=    10000; // interval for task monitoring
unsigned int MONITOR_QUEUE_DELAY_MS=   10000; // interval for queue monitoring
// ============================================
// =============Fuction declaration============
void TaskMonitor(void *pvParameters);
void TaskQueueMonitor(void *pvParameters);

TaskHandle_t Task_QueueMonitor_Handle;
TaskHandle_t Task_Monitor_Handle;


extern TaskHandle_t Task_LED_Handle;
extern TaskHandle_t Task_FSRRead_Handle;
extern TaskHandle_t Task_BLE_Handle;
extern TaskHandle_t Task_TimeKeeper_Handle;
extern TaskHandle_t Task_LocalTimerWacher_Handle;



extern QueueHandle_t FSR_fifo; // fifo for the FSR data
extern QueueHandle_t t0Queue; // Fifo for the change of time


// ============================================

// Arrays containing the tasks and queues that will be inspected.
static MonitoredTask monitoredTasks[] =
{
        {"TaskMonitor",&Task_Monitor_Handle},
        {"TaskQueueMonitor",&Task_QueueMonitor_Handle},
        {"Task_LED",&Task_LED_Handle},
        {"Task_FSR",&Task_FSRRead_Handle},
        {"Task_BLE",&Task_BLE_Handle},
        {"Task_TimeKeeper",&Task_TimeKeeper_Handle},
        {"TaskLocalTimerWatcher",&Task_LocalTimerWacher_Handle},
};

static MonitoredQueue monitoredQueues[] =
{
        {"Q FSR",&FSR_fifo},
        {"Q T0",&t0Queue},
};


// ========== FUNCIONES MONITOR ==============

// Print stack and heap usage for all monitored tasks.
void TaskMonitor(void *pvParameters)
{
        while (true)
        {
                printf("\n====== MONITOR DE SISTEMA ======\n");

                for (auto &task : monitoredTasks) {
                        if (*(task.handle)) {
                                printf("[%s]   Prio: %2u | Stack libre min: %4u bytes\n",
                                        task.name,
                                        uxTaskPriorityGet(*(task.handle)),
                                        uxTaskGetStackHighWaterMark(*(task.handle)) * sizeof(StackType_t));
                        }
                }

                printf("\nHeap actual disponible: %u bytes\n", (unsigned int)esp_get_free_heap_size());
                printf("Heap mínimo histórico:  %u bytes\n", (unsigned int)esp_get_minimum_free_heap_size());
                printf("====================================\n");

                vTaskDelay(pdMS_TO_TICKS(MONITOR_TASK_DELAY_MS));
        }
}

// Print occupancy statistics for all monitored queues.
void TaskQueueMonitor(void *pvParameters)
{
        while (true)
        {
                printf("\n====== 📦 MONITOR DE COLAS FIFO ======\n");

                for (auto &queue : monitoredQueues) {
                        if (*(queue.handle)) {
                                UBaseType_t used = uxQueueMessagesWaiting(*(queue.handle));
                                UBaseType_t free = uxQueueSpacesAvailable(*(queue.handle));
                                printf("[%s] Ocupado: %2u | Libre: %2u | Total: %u\n",
                                       queue.name, used, free, used + free);
                        }
                }

                printf("=======================================\n");
                vTaskDelay(pdMS_TO_TICKS(MONITOR_QUEUE_DELAY_MS));
        }
}

///////////////////////////////
