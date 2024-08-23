import sys
from PyQt5.QtWidgets import QApplication
from GUI import ArduinoGUI
from ArduinoSerialComm import SerialComm
from gestion_data import DataHandler

if __name__ == '__main__':
    app = QApplication(sys.argv)

    serial_comm = SerialComm()
    data_handler = DataHandler()

    gui = ArduinoGUI(serial_comm, data_handler)
    gui.show()

    sys.exit(app.exec_())
