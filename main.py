import sys
from PyQt5.QtWidgets import QApplication
from GUI import SerialMonitorApp

#main loop

"""
Inicio fácil

la idea general de como debe funcionar este programa es:
-boton para conectar al arduino
-boton para graficar
-boton para deconectar
-gráfica en tiempo real
-guardado en .csv

Manuel Mesa

"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialMonitorApp()
    window.show()
    sys.exit(app.exec_())
