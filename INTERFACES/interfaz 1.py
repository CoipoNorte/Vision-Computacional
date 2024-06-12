from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

app = QApplication([])
ventana = QMainWindow()
ventana.setWindowTitle("Traductor LSCH")

widget_central = QWidget()
layout = QGridLayout()

# Esquina superior izquierda: título y descripción
titulo = QLabel("Traductor LSCH\nPrototipo VC")
titulo.setFont(QFont('Arial', 20))
titulo.setStyleSheet("background-color: lightblue; border-radius: 15px; padding: 10px;")
layout.addWidget(titulo, 0, 0)

# Esquina inferior izquierda: descripción de los botones
descripcion = QLabel("Descripción de los botones")
descripcion.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px; color: gray;")
layout.addWidget(descripcion, 1, 0)

# Esquina superior derecha: botón "TRADUCIR"
boton_traducir = QPushButton("TRADUCIR")
boton_traducir.setStyleSheet("background-color: blue; color: white; border-radius: 15px; font-size: 20px;")
layout.addWidget(boton_traducir, 0, 1)

# Esquina inferior derecha: botones de colores
colores = ['lightgreen', 'blue', 'lightblue', 'yellow']
for i in range(2):
    for j in range(2):
        boton = QPushButton("Traducir Palabra")
        boton.setStyleSheet(f"background-color: {colores[i*2+j]}; border-radius: 15px;")
        layout.addWidget(boton, i+1, j+1)

widget_central.setLayout(layout)
ventana.setCentralWidget(widget_central)
ventana.show()

app.exec_()
