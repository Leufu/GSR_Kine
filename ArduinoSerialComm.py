#Moldularización del código
#Mientras más ordenado se entiende más y podré avanzar

#crear una clase para Comm

import serial
import time

class SerialComm:
    def __init__(self, port=None, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None

    def connect(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Esperar a que el Arduino se reinicie
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def read_line(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                return self.serial_port.readline().decode('utf-8').strip()
            except Exception as e:
                print(f"Error de lectura: {e}")
                return None
        return None

    def disconnect(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
