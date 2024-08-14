""""
La idea de este código es ser la interfaz de usuario
-Ser GUI idealmente
-Tiene que mostrar un grafico en tiempo real de lo  que esta midiendo
-Queremos enteregue un .CSV (¿?) para leer en excel

Manuel Mesa 
13/08/24
"""""
# Librerias
# Recordar agregarlas para los requirements.txt déspues, con sus respectivas versiones

import tkinter as tk

#Clase app para arduino

class ArduinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de datos Arduino")
        self.arduino_connected = False
        self.serial_port = None
        self.data = []

# Agregar un deslizador con los puertos en el cual se va a conectar el dispositivo al PC
# 
# Boton que para comprobar conexión
#
# Agregar algún icono que indique el estado del Arduino conectado/desconectado

# Mostrar grafico y valores mientras se esta midiendo
# Sacar los valores de arduino (??)
# USAR serial graph del mismo arduino ???
# Boton para inicio/paro de graficar en tiempo real

# Guardar en CSV
# abre comienze a guardar
# cierre, guarda archivo con los valores, con fecha y hora de la muestra de los datos
# Boton desde cuando hasta cuando grabar datos (Puede ser Grabar: inicio/stop)


#Funciones


#main loop

if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoGUI(root)
    root.mainloop()