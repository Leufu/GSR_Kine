from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QMessageBox
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import ArduinoSerialComm
import gestion_data

class ArduinoGUI(QMainWindow):
    def __init__(self, serial_comm, data_handler):
        super().__init__()

        self.comm = serial_comm
        self.data_handler = data_handler
        self.graphing = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Arduino GUI')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        self.port_dropdown = QComboBox()
        self.update_ports()
        main_layout.addWidget(self.port_dropdown)

       # self.get_available_ports = QPushButton('Actualizar')
       # self.get_available_ports.clicked.get_available_ports(self.get_available_portss)
       # main_layout.addWidget(self.connect_button)

        self.connect_button = QPushButton('Conectar')
        self.connect_button.clicked.connect(self.connect_serial)
        main_layout.addWidget(self.connect_button)

        self.status_label = QLabel('Estado: Desconectado')
        main_layout.addWidget(self.status_label)

        self.start_button = QPushButton('Iniciar Graficación')
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_graph)
        main_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Detener Graficación')
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_graph)
        main_layout.addWidget(self.stop_button)

        self.save_button = QPushButton('Guardar Datos')
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_csv)
        main_layout.addWidget(self.save_button)

        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setLabel('left', 'Valor')
        self.graph_widget.setLabel('bottom', 'Muestra')
        self.graph_widget.setTitle("Graficación en Tiempo Real")
        main_layout.addWidget(self.graph_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)

    def update_ports(self):
        self.port_dropdown.clear()
        self.port_dropdown.addItems(self.comm.get_available_ports())

    def connect_serial(self):
        self.comm.port = self.port_dropdown.currentText()
        if self.comm.connect():
            self.status_label.setText("Estado: Conectado")
            self.connect_button.setEnabled(False)
            self.start_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Error de Conexión", f"No se pudo conectar al puerto {self.comm.port}")

    def start_graph(self):
        self.graphing = True
        self.data_handler.data = []
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.save_button.setEnabled(False)
        self.timer.start(1)

    def stop_graph(self):
        self.graphing = False
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.save_button.setEnabled(True)

    def update_graph(self):
        if self.graphing:
            line = self.comm.read_line()
            if line:
                try:
                    value = float(line)
                    self.data_handler.add_data(value)
                    self.graph_widget.plot(self.data_handler.get_data(), clear=True, pen=pg.mkPen(color='b', width=2))
                except ValueError:
                    pass

    def save_csv(self):
        self.data_handler.save_csv(self)
