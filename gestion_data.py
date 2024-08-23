import csv
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class DataHandler:
    def __init__(self):
        self.data = []

    def add_data(self, value):
        self.data.append(value)
        if len(self.data) > 10:  # Limitar tamaño de los datos
            self.data.pop(0)
    #funcion que borra la cola
#    def delete_data(self,value):
#        self.data.


    def get_data(self):
        return self.data

    def save_csv(self, parent):
        if self.data:
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(parent, "Guardar Datos", "", "CSV Files (*.csv);;All Files (*)", options=options)
            if filename:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Muestra", "Valor"])
                    for i, value in enumerate(self.data):
                        writer.writerow([i, value])
                QMessageBox.information(parent, "Guardado", f"Datos guardados en {filename}")
