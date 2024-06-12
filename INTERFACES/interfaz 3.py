from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

app = QApplication([])
ventana = QMainWindow()
ventana.setWindowTitle("Traductor LSCH")

widget_central = QWidget()
layout = QGridLayout()

# Esquina superior izquierda: título y descripción
titulo = QLabel("Traductor LSCH")
titulo.setFont(QFont('Arial', 20))
titulo.setStyleSheet("background-color: #0071D5; border-radius: 15px; padding: 10px; color: white;")
titulo.setAlignment(Qt.AlignCenter)
layout.addWidget(titulo, 0, 0)

subtitulo = QLabel("Prototipo VC")
subtitulo.setFont(QFont('Arial', 15))
subtitulo.setStyleSheet("background-color: #0071D5; border-radius: 15px; padding: 10px; color: white;")
subtitulo.setAlignment(Qt.AlignCenter)
layout.addWidget(subtitulo, 1, 0)

descripcion = QLabel("Este prototipo tiene como objetivo exponer la capacidad de la Vision Computacional para el reconocimiento continuo de las palabras en la lengua de señas chilana")
descripcion.setStyleSheet("background-color: #0071D5; border-radius: 15px; padding: 10px; color: white;")
descripcion.setAlignment(Qt.AlignCenter)
layout.addWidget(descripcion, 2, 0)

# Esquina inferior izquierda: descripción de los botones
instrucciones = QLabel("Capturar: Grabar una nueva palabra\nTratar: Limpieza del Video.\nAprender: Agregar palabra al diccionario.\nReconocer: Traducir palabras.")
instrucciones.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px; color: gray;")
instrucciones.setAlignment(Qt.AlignCenter)
layout.addWidget(instrucciones, 3, 0)

# Esquina superior derecha: botón "TRADUCIR"
boton_traducir = QPushButton("Reconocer\nTraducir LSCH")
boton_traducir.setStyleSheet("background-color: #0071D5; color: white; border-radius: 15px; font-size: 20px;")
boton_traducir.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
layout.addWidget(boton_traducir, 0, 1, 2, 1)  # El botón ocupa 2 filas

# Esquina inferior derecha: botones de colores
colores = ['#0085FC', '#33A64C', '#FFBC26', '#1CA5B8']
for i in range(2):
    for j in range(2):
        boton = QPushButton("Traducir Palabra")
        boton.setStyleSheet(f"background-color: {colores[i*2+j]}; border-radius: 15px; color: white;")
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(boton, i+2, j+1)  # Los botones empiezan en la fila 2

widget_central.setLayout(layout)
ventana.setCentralWidget(widget_central)
ventana.show()

app.exec_()
