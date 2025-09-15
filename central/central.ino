#include <Arduino.h>
#include <NimBLEDevice.h>

static const NimBLEAdvertisedDevice* advDevice = nullptr;
static bool                          doConnect  = false;
static uint32_t                      scanTimeMs = 5000; // 0 = escanear por siempre

// Solo conectamos a este servicio:
static const NimBLEUUID targetServiceUUID("A002");

// ——— Notificaciones/indicaciones: SOLO mostrar "value=" ———
static void notifyCB(NimBLERemoteCharacteristic* pChr, uint8_t* pData, size_t length, bool isNotify) {
    // Si parece ASCII imprimimos crudo; si no, en hex
    bool asciiish = true;
    for (size_t i = 0; i < length; ++i) {
        uint8_t b = pData[i];
        if (b < 0x09 || b > 0x7E) { asciiish = false; break; }
    }

    //Serial.print("value=");
    if (asciiish) {
        Serial.write(pData, length);
    } else {
        for (size_t i = 0; i < length; ++i) {
            if (i) Serial.print(' ');
            char buf[4];
            snprintf(buf, sizeof(buf), "%02X", pData[i]);
            Serial.print(buf);
        }
    }
    // Asegurar fin de línea
    if (length == 0 || (pData[length-1] != '\n' && pData[length-1] != '\r')) Serial.println();
}

// ——— Callbacks de cliente (mínimos) ———
class ClientCallbacks : public NimBLEClientCallbacks {
    void onConnect(NimBLEClient* /*pClient*/) override {}
    void onDisconnect(NimBLEClient* pClient, int /*reason*/) override {
        NimBLEDevice::getScan()->start(scanTimeMs, false, true);
    }
} clientCallbacks;

// ——— Callbacks de escaneo: elegir solo los que anuncien 0x180C ———
class ScanCallbacks : public NimBLEScanCallbacks {
    void onResult(const NimBLEAdvertisedDevice* advertisedDevice) override {
        if (advertisedDevice->isAdvertisingService(targetServiceUUID)) {
            NimBLEDevice::getScan()->stop();
            advDevice = advertisedDevice;
            doConnect = true;
        }
    }
    void onScanEnd(const NimBLEScanResults& results, int /*reason*/) override {
        // Reiniciar escaneo continuamente
        NimBLEDevice::getScan()->start(scanTimeMs, false, true);
    }
} scanCallbacks;

// ——— Conexión y suscripción a TODAS las características notificables del servicio 0x180C ———
static bool connectToServer() {
    NimBLEClient* pClient = nullptr;

    if (NimBLEDevice::getCreatedClientCount()) {
        pClient = NimBLEDevice::getClientByPeerAddress(advDevice->getAddress());
        if (pClient) {
            if (!pClient->connect(advDevice, false)) return false;
        } else {
            pClient = NimBLEDevice::getDisconnectedClient();
        }
    }

    if (!pClient) {
        if (NimBLEDevice::getCreatedClientCount() >= NIMBLE_MAX_CONNECTIONS) return false;
        pClient = NimBLEDevice::createClient();
        pClient->setClientCallbacks(&clientCallbacks, false);
        pClient->setConnectionParams(12, 12, 0, 150);
        pClient->setConnectTimeout(5000);
        if (!pClient->connect(advDevice)) {
            NimBLEDevice::deleteClient(pClient);
            return false;
        }
    }

    if (!pClient->isConnected()) {
        if (!pClient->connect(advDevice)) return false;
    }

    // Solo servicio 0x180C
    NimBLERemoteService* pSvc = pClient->getService(targetServiceUUID);
    if (!pSvc) return false;

    // Enumerar características y suscribirse a las notificables/indicables
    auto clist = pSvc->getCharacteristics(true); // vector<NimBLERemoteCharacteristic*>
    for (auto* c : clist) {
        if (c->canNotify()) {
            c->subscribe(true, notifyCB);      // NOTIFY
        } else if (c->canIndicate()) {
            c->subscribe(false, notifyCB);     // INDICATE
        }
        // No imprimimos nada aquí; solo nos interesa el "value=" desde notifyCB
    }
    return true;
}

void setup() {
    Serial.begin(115200);
    while (!Serial) { delay(10); }

    NimBLEDevice::init("NimBLE-Client");

    // Potencia TX al máximo (~+9 dBm)
    NimBLEDevice::setPower(ESP_PWR_LVL_P9); // máximo disponible
    // Si tu core no define ESP_PWR_LVL_P9, usa: NimBLEDevice::setPower(9);

    NimBLEScan* pScan = NimBLEDevice::getScan();
    pScan->setScanCallbacks(&scanCallbacks, false);
    pScan->setInterval(100);
    pScan->setWindow(100);
    pScan->setActiveScan(true);
    pScan->start(scanTimeMs);
}

void loop() {
    delay(10);
    if (doConnect) {
        doConnect = false;
        if (!connectToServer()) {
            // si falla, retomamos escaneo
        }
        NimBLEDevice::getScan()->start(scanTimeMs, false, true);
    }
}

