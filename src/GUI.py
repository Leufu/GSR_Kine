"""
La clase de la conexión la deje aparte,
la del plot esta en este código, puede ser mejorado a futuro
aquí con la libreria PyQt5 se hace la interfaz

la idea general de como debe funcionar este programa es:
-botón para conectar al arduino
-botón para graficar
-botón para deconectar
-gráfica en tiempo real
-guardado en .csv

"""
import sys
import csv
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QFileDialog, QLabel
import pyqtgraph as pg
from serial_communication import SerialCommunication

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

        # Botón para refrescar puertos
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_ports)
        layout.addWidget(self.refresh_button)

        # Botón para conectar
        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.connect_serial)
        layout.addWidget(self.connect_button)

        # Botón para desconectar
        self.disconnect_button = QPushButton("Desconectar")
        self.disconnect_button.clicked.connect(self.disconnect_serial)
        self.disconnect_button.setEnabled(False)
        layout.addWidget(self.disconnect_button)

        # Etiqueta de estado
        #Etiqueta cuando se usó tkinter
        #self.status_label = tk.Label(self.root, text="Estado: Desconectado", fg="red")
        #self.status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # En pyQt
        self.status_label = QLabel("Status: Disconnected", self)
        layout.addWidget(self.status_label)

        # Botón para comenzar a graficar
        self.start_button = QPushButton("Iniciar Gráfica")
        self.start_button.clicked.connect(self.start_graph)
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)

        # Botón para PARAR a graficar
        self.stop_button = QPushButton("Detener Gráfica")
        self.stop_button.clicked.connect(self.stop_graph)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        # Botón para REINICIAR la grafica
        self.reset_button = QPushButton("Reiniciar Gráfica")
        self.reset_button.clicked.connect(self.reset_graph)
        self.reset_button.setEnabled(False)
        layout.addWidget(self.reset_button)

        # Gráfica en Tkinter
        
        # Botón para iniciar la graficación
        # self.start_button = tk.Button(self.root, text="Iniciar Graficación", command=self.start_graph, state="disabled")
        # self.start_button.grid(row=2, column=0, padx=10, pady=10)

        # Botón para detener la graficación
        # self.stop_button = tk.Button(self.root, text="Detener Graficación", command=self.stop_graph, state="disabled")
        # self.stop_button.grid(row=2, column=1, padx=10, pady=10)

        # Gráfico
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # Establecer fondo blanco
        self.plot_widget.showGrid(x=True, y=True) # cuadriculado
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
            self.status_label.setText(f"Status: Connected to {port}")  # Actualizar la QLabel
            self.status_label.setStyleSheet("color: green;")  # Cambiar color a verde
        else:
            QMessageBox.critical(self, "Error", f"No se pudo conectar al puerto {port}")
    
    def update_ports(self):
        ports = self.serial_comm.get_available_ports()
        self.port_dropdown.clear()
        self.port_dropdown.addItems(ports)

# En Tkinter

#    def start_graph(self):
#        self.graphing = True
#        self.data = []
#        self.start_button.config(state="disabled")
#        self.stop_button.config(state="normal")
#        self.save_button.config(state="disabled")
#        self.update_graph()

#    def stop_graph(self):
#        self.graphing = False
#        self.stop_button.config(state="disabled")
#        self.start_button.config(state="normal")
#        self.save_button.config(state="normal")

#comienza la gráfica

    def start_graph(self):
        self.data = []
        self.timestamps = []
        self.start_time = time.time()
        self.timer.start(50)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.save_button.setEnabled(True)

#   def start_graph(self):
#        self.data = []
#        self.timestamps = []
#        self.start_time = time.time()
#        self.timer.start(50)
#        self.start_button.setEnabled(False)
#        self.stop_button.setEnabled(True)
#        self.reset_button.setEnabled(True)
#        self.save_button.setEnabled(True) 

    def stop_graph(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def reset_graph(self):
        self.stop_graph()
        self.data.clear()
        self.timestamps.clear()
        self.plot.clear()
        self.start_graph()

#cierre de desconexión
    def disconnect_serial(self):
        self.timer.stop()
        self.serial_comm.disconnect()
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.status_label.setText("Status: Disconnected")  # Actualizar la QLabel
        self.status_label.setStyleSheet("color: red;")  # Cambiar color a rojo
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
