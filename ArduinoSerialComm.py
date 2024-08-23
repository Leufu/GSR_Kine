import serial
import serial.tools.list_ports

class SerialComm:
    def __init__(self):
        self.ser = None
        self.port = None
        self.baudrate = 9600

    def get_available_ports(self):
        port_devices = []
        for port in serial.tools.list_ports.comports():
            if "USB-SERIAL" in port.description: 
                port_devices.append(port.device)
        return port_devices

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        if self.ser:
            self.ser.close()
            self.ser = None

    def read_line(self):
        if self.ser:
            return self.ser.readline().decode().strip()
        return None
