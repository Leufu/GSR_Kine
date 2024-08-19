import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import serial.tools.list_ports
import time
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Clase app para arduino

class ArduinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino GUI")

        self.arduino_connected = False
        self.serial_port = None
        self.data = []

        self.create_widgets()

    def create_widgets(self):
        self.port_var = tk.StringVar()
# Interfaz gráfica
# Agregar una lista desplegable con los puertos en el cual se va a conectar el dispositivo al PC 

        # Lista desplegable de puertos
        self.port_menu = ttk.OptionMenu(self.root, self.port_var, "Select Port")
        self.port_menu.grid(row=0, column=0, padx=10, pady=10)

        # Botón para actualizar puertos
        self.refresh_button = tk.Button(self.root, text="Actualizar Puertos", command=self.update_ports)
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10)

        # Botón de conexión
        self.connect_button = tk.Button(self.root, text="Conectar", command=self.connect_serial)
        self.connect_button.grid(row=0, column=2, padx=10, pady=10)

        # Etiqueta de estado
        self.status_label = tk.Label(self.root, text="Estado: Desconectado", fg="red")
        self.status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Botón para iniciar la graficación
        self.start_button = tk.Button(self.root, text="Iniciar Grafica", command=self.start_graph, state="disabled")
        self.start_button.grid(row=2, column=0, padx=10, pady=10)

        # Botón para detener la graficación
        self.stop_button = tk.Button(self.root, text="Detener Grafica", command=self.stop_graph, state="disabled")
        self.stop_button.grid(row=2, column=1, padx=10, pady=10)

        # Botón para guardar en CSV
        self.save_button = tk.Button(self.root, text="Guardar Datos", command=self.save_csv, state="disabled")
        self.save_button.grid(row=2, column=2, padx=10, pady=10)

        # Configuración de Matplotlib para graficar
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Guardar en CSV
# abre comienze a guardar
# cierre, guarda archivo con los valores, con fecha y hora de la muestra de los datos
# Boton desde cuando hasta cuando grabar datos (Puede ser Grabar: inicio/stop)
# Mostrar grafico y valores mientras se esta midiendo
# Sacar los valores de arduino (??)
# USAR serial graph del mismo arduino ???
# Boton para inicio/paro de graficar en tiempo real

#########################
#19/08/24
# El problema:
# Si me equivoco de puerto hay que cerrar por completo el programa
# Una vez conectado el puerto deberia haber una opción para hacer desconexión
# 
#
#########################
#Funciones
    # Inicializar la lista de puertos disponibles
        
    #Actualizar puertos
    def update_ports(self):
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        if not self.available_ports:
            self.available_ports = ["No ports found"]

        self.port_var.set(self.available_ports[0])
        menu = self.port_menu['menu']
        menu.delete(0, 'end')
        for port in self.available_ports:
            menu.add_command(label=port, command=lambda p=port: self.port_var.set(p))
    #Conexión a Arduino
    def connect_serial(self):
        port = self.port_var.get()
        try:
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)
            self.arduino_connected = True
            self.status_label.config(text="Estado: Conectado", fg="green")
            self.connect_button.config(state="disabled")
            self.start_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {port}\n{str(e)}")

#Funciones para la gráfica
#Iniciar grafica con un CSV vacío para comenzar a guardar datos

    def start_graph(self):
        self.graphing = True
        self.data = []
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.update_graph()

#Parar de gráficar

    def stop_graph(self):
        self.graphing = False
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.save_button.config(state="normal")

#Actualización del gráfico

    def update_graph(self):
        if self.graphing:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                if line:
                    value = float(line)
                    self.data.append(value)
                    self.ax.clear()
                    self.ax.plot(self.data)
                    self.canvas.draw()
            except Exception as e:
                self.stop_graph()
                messagebox.showerror("Error de Lectura", f"Error al leer del puerto serial\n{str(e)}")
                        # Llama a update_graph después de 100 ms
            self.root.after(100, self.update_graph)

#Guardar el CSV

    def save_csv(self):
        if self.data:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "Value"])
                    for i, value in enumerate(self.data):
                        writer.writerow([i, value])
                messagebox.showinfo("Guardado", f"Datos guardados en {filename}")

#Main Loop

if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoGUI(root)
    root.mainloop()