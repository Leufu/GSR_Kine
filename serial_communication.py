import serial
import serial.tools.list_ports
"""
Clase para la conexión a Arduino,
tiene la gracia de que reconoce solamente los puertos USB donde hay algún arduino

"""
class SerialCommunication:
    def __init__(self):
        self.ser = None
        self.port = None
        self.baudrate = 9600
#busca los puertos en el sistema
    def get_available_ports(self):
        port_devices = []
        #Aquí filtra con las variables de los puertos y com resultado solo los: USB-Serial (es decir arduinos, pueden ser otras cosas, pero es primer acercamiento)
        for port in serial.tools.list_ports.comports():
            if "USB-SERIAL" in port.description:
                port_devices.append(port.device)
        print(f"Available ports: {port_devices}")  # Depuración
        return port_devices
#establece la conexión
    def connect(self, port):
        try:
            print(f"Trying to connect to {port}...")  # Depuración
            self.ser = serial.Serial(port, self.baudrate, timeout=1)
            print(f"Connected to {port}")  # Depuración
            return True
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")  # Depuración
            return False
#deconectar
    def disconnect(self):
        if self.ser:
            print(f"Disconnecting from {self.ser.port}")  # Depuración
            self.ser.close()
            self.ser = None
#lectura de la linea
    def read_data(self):
        if self.ser:
#            print("Starting to read data...")  # Depuración
            while self.ser.is_open:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
#                    print(f"Read line: {line}")  # Depuración
#desafortunadamente con callback me tiraba errores que no pude solucionar, asi que preferi tener un float
                    if line.isnumeric():
                        return float(line)
                except serial.SerialException as e:
                    print(f"Serial exception: {e}")  # Depuración
                    break
            print("Stopped reading data.")  # Depuración
