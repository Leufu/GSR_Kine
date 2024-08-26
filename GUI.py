import sys
import csv
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QFileDialog
import pyqtgraph as pg
from serial_communication import SerialCommunication

"""
La clase de la conexión la deje aparte,
la del plot esta en este código, puede ser mejorado a futuro
aquí con la libreria PyQt5 se hace la interfaz

la idea general de como debe funcionar este programa es:
-boton para conectar al arduino
-boton para graficar
-boton para deconectar
-gráfica en tiempo real
-guardado en .csv

Comentaré en el codigo su funcionamiento

"""


class SerialMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
#titulo ventana
        self.setWindowTitle("Proyecto GSR Kine")
        self.setGeometry(100, 100, 800, 600)

        self.serial_comm = SerialCommunication()
        self.data = []
        self.timestamps = []
        self.start_time = None

        # Layout principal
        layout = QVBoxLayout()

        # Dropdown para seleccionar puerto
        self.port_dropdown = QComboBox()
        self.port_dropdown.addItems(self.serial_comm.get_available_ports())
        layout.addWidget(self.port_dropdown)

        # Botón para conectar
        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.connect_serial)
        layout.addWidget(self.connect_button)

        # Botón para comenzar a graficar
        self.start_button = QPushButton("Iniciar Gráfica")
        self.start_button.clicked.connect(self.start_graph)
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)

        # Botón para desconectar
        self.disconnect_button = QPushButton("Desconectar")
        self.disconnect_button.clicked.connect(self.disconnect_serial)
        self.disconnect_button.setEnabled(False)
        layout.addWidget(self.disconnect_button)

        # Gráfico
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # Establecer fondo blanco
        self.plot = self.plot_widget.plot([], [], pen='b')
        layout.addWidget(self.plot_widget)

        # Botón para guardar datos
        self.save_button = QPushButton("Guardar CSV")
        self.save_button.clicked.connect(self.save_csv)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        # Widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer para actualizar la gráfica
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

#conecta el arduino

    def connect_serial(self):
        port = self.port_dropdown.currentText()
        if self.serial_comm.connect(port):
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.start_button.setEnabled(True)
            QMessageBox.information(self, "Conectado", f"Conectado al puerto {port}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo conectar al puerto {port}")

#comienza la gráfica

    def start_graph(self):
        self.data = []
        self.timestamps = []
        self.start_time = time.time()
        self.timer.start(50)
        self.start_button.setEnabled(False)
        self.save_button.setEnabled(True)

#cierre de desconexión
    def disconnect_serial(self):
        self.timer.stop()
        self.serial_comm.disconnect()
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.start_button.setEnabled(False)
        QMessageBox.information(self, "Desconectado", "Conexión cerrada.")

#aquí se hace el "Scrolling window/plot"
    def update_plot(self):
        value = self.serial_comm.read_data()
        if value is not None:
            current_time = time.time() - self.start_time
            self.timestamps.append(current_time)
            self.data.append(value)
            self.plot.setData(self.timestamps, self.data)
            self.plot_widget.setXRange(max(0, current_time - 10), current_time)  # Scrolling effect

#guardado en .CSV
    def save_csv(self):
        if self.data:
            filename, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "", "CSV files (*.csv)")
            if filename:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "Value"])
                    for timestamp, value in zip(self.timestamps, self.data):
                        writer.writerow([timestamp, value])
                QMessageBox.information(self, "Guardado", f"Datos guardados en {filename}")
