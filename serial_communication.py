"""
Clase para la conexión a Arduino,
tiene la gracia de que reconoce solamente los puertos USB donde hay algún arduino
Tambien ahora tiene pensado un buffer
"""
import serial
import serial.tools.list_ports
import threading
import time
import csv

class SerialCommunication:
    def __init__(self, buffer_size=100, csv_filename="data.csv"):
        self.ser = None
        self.port = None
        self.baudrate = 9600
        self.lock = threading.Lock()
        self.buffer = []
        self.buffer_size = buffer_size
        self.current_filename = csv_filename

    def get_available_ports(self):
        port_devices = []
        for port in serial.tools.list_ports.comports():
            if "USB-SERIAL" in port.description:
                port_devices.append(port.device)
        print(f"Available ports: {port_devices}")  # Depuración
        return port_devices

    def connect(self, port):
        try:
            print(f"Trying to connect to {port}...")  # Depuración
            self.ser = serial.Serial(port, self.baudrate, timeout=1)
            print(f"Connected to {port}")  # Depuración
            return True
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")  # Depuración
            return False

    def disconnect(self):
        if self.ser:
            print(f"Disconnecting from {self.ser.port}")  # Depuración
            self.ser.close()
            self.ser = None

    def read_data(self):
        if self.ser and self.ser.is_open:
            try:
                line = self.ser.readline().decode('utf-8').strip()
     #           print(f"Read line: {line}")  # Depuración
                if line.isnumeric():
                    data = float(line)
                    self.add_to_buffer(data)
                    return data
            except serial.SerialException as e:
                print(f"Serial exception: {e}")  # Depuración
        return None

# funciones referentes al buffer
#toma los datos y los deja en el buffer
    def add_to_buffer(self, data):
        with self.lock:
            self.buffer.append((time.time(), data))
            if len(self.buffer) >= self.buffer_size:
                self.flush_buffer_to_csv()
#del buffer al csv
    def flush_buffer_to_csv(self):
        if self.current_filename:
            with open(self.current_filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.buffer)
                self.buffer.clear()
#guardado del resto al buffer
    def save_remaining_buffer(self):
        with self.lock:
            if self.buffer:
                self.flush_buffer_to_csv()
    