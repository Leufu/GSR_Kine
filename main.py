import sys
from PyQt5.QtWidgets import QApplication
from GUI import SerialMonitorApp

#main loop

"""
Inicio fácil

La idea general de como debe funcionar este programa es:

-botón para conectar al Arduino
-botón para graficar
-botón para desconectar
-gráfica en tiempo real
-guardado en .csv

Manuel Mesa

Contiene tres archivos:

main.py:
Archivo que contiene el loop principal de la "app"

GUI.py:
Aquí está la interfaz,
con sus funciones y widgets 
llama las funciones de la clase de la comincación con el arduino que esta en el otro archivo

serial_communication.py:
Aquí la clase para comunicar con el arduino,
conecta, desconecta, pide datos, etc.

"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialMonitorApp()
    window.show()
    sys.exit(app.exec_())
