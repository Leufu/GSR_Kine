import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from ArduinoSerialComm import SerialComm  # Importar la clase de comunicación serial
import serial.tools.list_ports  # Importar para obtener los puertos disponibles

class ArduinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino GUI")

        self.comm = SerialComm()
        self.data = []
        self.graphing = False

        self.create_widgets()

    def create_widgets(self):
        self.port_var = tk.StringVar()

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
        self.start_button = tk.Button(self.root, text="Iniciar Graficación", command=self.start_graph, state="disabled")
        self.start_button.grid(row=2, column=0, padx=10, pady=10)

        # Botón para detener la graficación
        self.stop_button = tk.Button(self.root, text="Detener Graficación", command=self.stop_graph, state="disabled")
        self.stop_button.grid(row=2, column=1, padx=10, pady=10)

        # Botón para guardar en CSV
        self.save_button = tk.Button(self.root, text="Guardar Datos", command=self.save_csv, state="disabled")
        self.save_button.grid(row=2, column=2, padx=10, pady=10)

        # Configuración de Matplotlib para graficar
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def update_ports(self):
        available_ports = [port.device for port in serial.tools.list_ports.comports()]
        if not available_ports:
            available_ports = ["No ports found"]

        self.port_var.set(available_ports[0])
        menu = self.port_menu['menu']
        menu.delete(0, 'end')
        for port in available_ports:
            menu.add_command(label=port, command=lambda p=port: self.port_var.set(p))

    def connect_serial(self):
        self.comm.port = self.port_var.get()
        if self.comm.connect():
            self.status_label.config(text="Estado: Conectado", fg="green")
            self.connect_button.config(state="disabled")
            self.start_button.config(state="normal")
        else:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {self.comm.port}")

    def start_graph(self):
        self.graphing = True
        self.data = []
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.update_graph()

    def stop_graph(self):
        self.graphing = False
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.save_button.config(state="normal")

    def update_graph(self):
        if self.graphing:
            line = self.comm.read_line()
            if line:
                try:
                    value = float(line)
                    self.data.append(value)
                    self.ax.clear()
                    self.ax.plot(self.data)
                    self.canvas.draw()
                except ValueError:
                    pass

            self.root.after(100, self.update_graph)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoGUI(root)
    root.mainloop()
