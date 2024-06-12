from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import subprocess

# Funciones para ejecutar los scripts
def ejecutar_capture_samples():
    subprocess.run(["python", "capture_samples.py"])

def ejecutar_create_keypoints():
    subprocess.run(["python", "create_keypoints.py"])

def ejecutar_training_model():
    subprocess.run(["python", "training_model.py"])

def ejecutar_evaluate_model():
    subprocess.run(["python", "evaluate_model.py"])

app = QApplication([])
ventana = QMainWindow()
ventana.setWindowTitle("Traductor LSCH")
ventana.setGeometry(200, 200, 800, 600)  # Tamaño inicial de la ventana

widget_central = QWidget()
layout = QGridLayout()

# Parte 1: Título, subtítulo y descripción
recuadro_superior_izquierda = QWidget()
recuadro_layout = QVBoxLayout()

titulo = QLabel("Traductor LSCH")
titulo.setFont(QFont('Arial', 20))
titulo.setStyleSheet("color: white;")
titulo.setAlignment(Qt.AlignCenter)

subtitulo = QLabel("Prototipo VC")
subtitulo.setFont(QFont('Arial', 16))
subtitulo.setStyleSheet("color: white;")
subtitulo.setAlignment(Qt.AlignCenter)

descripcion = QLabel("Este prototipo tiene como objetivo exponer la capacidad de la Vision Computacional para el reconocimiento continuo de las palabras en la lengua de señas chilena")
descripcion.setFont(QFont('Arial', 10))
descripcion.setStyleSheet("color: white;")
descripcion.setAlignment(Qt.AlignCenter)
descripcion.setWordWrap(True)

recuadro_layout.addWidget(titulo)
recuadro_layout.addWidget(subtitulo)
recuadro_layout.addWidget(descripcion)

recuadro_superior_izquierda.setLayout(recuadro_layout)
recuadro_superior_izquierda.setStyleSheet("background-color: #0071D5; border-radius: 15px; padding: 10px;")
layout.addWidget(recuadro_superior_izquierda, 0, 0)

# Parte 2: Botón "TRADUCIR"
boton_traducir = QPushButton("Reconocer\nTraducir LSCH")
boton_traducir.setStyleSheet("background-color: #005499; color: white; border-radius: 15px; font-size: 20px; padding: 30px; text-align: center;")
boton_traducir.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Establecer la política de tamaño fijo
layout.addWidget(boton_traducir, 0, 1, alignment=Qt.AlignHCenter)

# Parte 3: Descripción de los botones
descripcion_botones = QLabel("Capturar: Grabar una nueva palabra\nTratar: Limpieza del Video.\nAprender: Agregar palabra al diccionario.\nReconocer: Traducir palabras.")
descripcion_botones.setFont(QFont('Arial', 12))  # Tamaño de fuente aumentado
descripcion_botones.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px; color: gray;")
descripcion_botones.setAlignment(Qt.AlignCenter)
layout.addWidget(descripcion_botones, 1, 0)

# Parte 4: Cuatro botones de colores
botones_layout = QGridLayout()
textos_botones = ["Capturar\nnueva palabra", "Tratar\nla palabra", "Aprender\nla palabra", "Reconocer"]
colores = ['#0085FC', '#33A64C', '#FFBC26', '#1CA5B8']

botones = []  # Lista para almacenar los botones

for i in range(2):
    for j in range(2):
        boton = QPushButton(textos_botones[i*2+j])
        boton.setFont(QFont('Arial', 12))  # Tamaño de fuente aumentado
        boton.setStyleSheet(f"background-color: {colores[i*2+j]}; border-radius: 15px; color: white;")
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        botones_layout.addWidget(boton, i, j)
        botones.append(boton)  # Agregar el botón a la lista

botones_widget = QWidget()
botones_widget.setLayout(botones_layout)
layout.addWidget(botones_widget, 1, 1)

# Conectar botones a las funciones correspondientes
botones[0].clicked.connect(ejecutar_capture_samples)
botones[1].clicked.connect(ejecutar_create_keypoints)
botones[2].clicked.connect(ejecutar_training_model)
botones[3].clicked.connect(ejecutar_evaluate_model)

widget_central.setLayout(layout)
ventana.setCentralWidget(widget_central)
ventana.show()

app.exec_()
