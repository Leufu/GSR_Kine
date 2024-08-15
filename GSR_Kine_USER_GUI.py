""""
La idea de este código es ser la interfaz de usuario
-Ser GUI idealmente
-Tiene que mostrar un grafico en tiempo real de lo  que esta midiendo
-Queremos enteregue un .CSV para leer en excel

Manuel Mesa 
13/08/24
"""""
# Librerias
# Recordar agregarlas para los requirements.txt déspues, con sus respectivas versiones

import tkinter as tk
from tkinter import messagebox, filedialog
import serial
import serial.tools.list_ports
import time
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

#Clase app para arduino

class ArduinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de datos Arduino")

        self.serial_port = None
   
# Interfaz gráfica
# Agregar una lista desplegable con los puertos en el cual se va a conectar el dispositivo al PC 
        self.port_label = tk.Label(root, text="Selecciona el puerto:")
        self.port_label.pack(pady=5)



        self.port_var = tk.StringVar(root)
        self.port_menu = tk.OptionMenu(root, self.port_var, "")  # Inicia con un menú vacío
        self.port_menu.pack(pady=5)
#Actualizar puertos
        self.refresh_button = tk.Button(root, text="Actulizar Puertos", command=self.update_ports)
        self.refresh_button.pack(pady=5)

# Boton que para comprobar conexión
        self.connect_button = tk.Button(root, text="Conectar", command=self.connect_serial)
        self.connect_button.pack(pady=5)
# Agregar algún icono que indique el estado del Arduino conectado/desconectado
        self.status_label = tk.Label(root, text="Estado: Desconectado", fg="red")
        self.status_label.pack(pady=5)

        # Inicializar la lista de puertos disponibles
        self.update_ports()

# Mostrar grafico y valores mientras se esta midiendo



# Sacar los valores de arduino (??)
# USAR serial graph del mismo arduino ???
# Boton para inicio/paro de graficar en tiempo real



# Guardar en CSV
# abre comienze a guardar
# cierre, guarda archivo con los valores, con fecha y hora de la muestra de los datos
# Boton desde cuando hasta cuando grabar datos (Puede ser Grabar: inicio/stop)



#Funciones
    def update_ports(self):
        # Obtiene los puertos seriales disponibles
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        if not self.available_ports:
            self.available_ports = ["No ports found"]

        # Actualiza la lista desplegable
        self.port_var.set(self.available_ports[0])
        menu = self.port_menu['menu']
        menu.delete(0, 'end')
        for port in self.available_ports:
            menu.add_command(label=port, command=lambda p=port: self.port_var.set(p))

    def connect_serial(self):
        port = self.port_var.get()
        try:
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            self.status_label.config(text="Estado: Conectado", fg="green")
            self.connect_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {port}\n{str(e)}")
            self.status_label.config(text="Estado: Desconectado", fg="red")


# Configuración de Matplotlib


        # Variables de control

        #Puertos

        #Conectado de arduino

#main loop

if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoGUI(root)
    root.mainloop()