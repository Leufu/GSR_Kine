//#include <esp32-hal-bt.c>

// BLE configuration for the peripheral foot device.
#include <NimBLEDevice.h>
#define	size_of_struct 12000
#define  chunk_size 128

// Configuration for the BLE service used to transmit FSR data.
const char* matrixUUID= "A002";
//BLEService sensorService(matrixUUID);
//BLEStringCharacteristic sensorCharacteristic(matrixUUID,BLERead | BLENotify,128);

// Creation of the server, service and characteristic for sending data
static NimBLEServer* pServer = nullptr;
static NimBLEService* pSensorService = nullptr;
static NimBLECharacteristic* pSensorCharacteristic = nullptr;






// Initializes the BLE stack, service and characteristic for data transmission.
void Init_BLE()
{	

  //NimBLEDevice::init();
  NimBLEDevice::init("Peripheral_GSR");
  //NimBLEAdvertising::enableScanResponse()
	//NimBLEAdvertising::setName("name1");
		//NimBLEAdvertisementData::setName("name2");
  NimBLEDevice::setMTU(256); //setMTU after init the BLEDEVICE XDD else crash 
	//if (!NimBLEDevice::setDeviceName("Sick-FSR-insole")) 
	////{Serial.print("Name not changed");}
  pServer = NimBLEDevice::createServer();

  // Crear servicio
  pSensorService = pServer->createService(matrixUUID);

  // Crear característica con notificación
  pSensorCharacteristic = pSensorService->createCharacteristic(
    matrixUUID,
    NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
  );

  // Valor inicial
  pSensorCharacteristic->setValue("0");

  // Iniciar el servicio
  pSensorService->start();

  // Configurar publicidad
  NimBLEAdvertising* pAdvertising = NimBLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(pSensorService->getUUID());
  ////pAdvertising->setScanResponse(true);
  pAdvertising->enableScanResponse(true);
  pAdvertising->start();

  pAdvertising->enableScanResponse(true);
  //pAdvertising->setScanResponseData(true);
  Serial.println("GSR (Sending Data) - NimBLE iniciado");
  Serial.printf("MTU = %i",NimBLEDevice::getMTU() );
  
  // en tu Init_BLE()
	//NimBLEDevice::setLogLevel(LOG_LEVEL_NONE);


}



