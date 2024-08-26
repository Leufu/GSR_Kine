import sys
from PyQt5.QtWidgets import QApplication
from GUI import SerialMonitorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialMonitorApp()
    window.show()
    sys.exit(app.exec_())
