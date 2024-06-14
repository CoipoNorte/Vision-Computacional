import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QSizePolicy, QLineEdit
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class WebcamWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Establecer el ancho del frame
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Establecer la altura del frame

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Traductor LSCH")
        self.setGeometry(100, 100, 1030, 640)  # Tamaño inicial de la ventana

        self.widget_central = QWidget()
        self.layout = QGridLayout()

        # Parte 1: Título, subtítulo y descripción
        self.recuadro_superior_izquierda = QWidget()
        self.recuadro_layout = QVBoxLayout()

        self.titulo = QLabel("Traductor LSCH")
        self.titulo.setFont(QFont('Arial', 20))
        self.titulo.setStyleSheet("color: white;")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.subtitulo = QLabel("Prototipo VC")
        self.subtitulo.setFont(QFont('Arial', 16))
        self.subtitulo.setStyleSheet("color: white;")
        self.subtitulo.setAlignment(Qt.AlignCenter)

        self.descripcion = QLabel("Ingrese una nueva palabra:")
        self.descripcion.setFont(QFont('Arial', 12))
        self.descripcion.setStyleSheet("color: white;")
        self.descripcion.setAlignment(Qt.AlignCenter)

        self.palabra_ingresada = QLineEdit()
        self.palabra_ingresada.setFont(QFont('Arial', 12))
        self.palabra_ingresada.setStyleSheet("background-color: white; color: black;")
        self.palabra_ingresada.setAlignment(Qt.AlignCenter)

        self.recuadro_layout.addWidget(self.titulo)
        self.recuadro_layout.addWidget(self.subtitulo)
        self.recuadro_layout.addWidget(self.descripcion)
        self.recuadro_layout.addWidget(self.palabra_ingresada)

        self.recuadro_superior_izquierda.setLayout(self.recuadro_layout)
        self.recuadro_superior_izquierda.setStyleSheet("background-color: #0071D5; border-radius: 15px; padding: 10px;")
        self.layout.addWidget(self.recuadro_superior_izquierda, 0, 0)

        # Parte 2: Vista de la cámara
        self.camera_widget = WebcamWidget()
        self.layout.addWidget(self.camera_widget, 0, 1, 2, 1)  # Ahora está en la columna 1 y ocupa dos filas

        # Parte 3: Descripción de los botones
        self.descripcion_botones = QLabel(" ")
        self.descripcion_botones.setFont(QFont('Arial', 12))  # Tamaño de fuente aumentado
        self.descripcion_botones.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px; color: gray;")
        self.descripcion_botones.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.descripcion_botones, 2, 0)

        # Parte 4: Cuatro botones de colores
        self.botones_layout = QGridLayout()
        self.textos_botones = ["Nueva palabra", "Puntos caracteristicos", "Aprender palabra", "Reconocer"]
        self.colores = ['#0085FC', '#33A64C', '#FFBC26', '#1CA5B8']

        for i in range(2):
            for j in range(2):
                self.boton = QPushButton(self.textos_botones[i*2+j])
                self.boton.setFont(QFont('Arial', 12))  # Tamaño de fuente aumentado
                self.boton.setStyleSheet(f"background-color: {self.colores[i*2+j]}; border-radius: 15px; color: white;")
                self.boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.botones_layout.addWidget(self.boton, i, j)

        self.botones_widget = QWidget()
        self.botones_widget.setLayout(self.botones_layout)
        self.layout.addWidget(self.botones_widget, 2, 1)

        self.widget_central.setLayout(self.layout)
        self.setCentralWidget(self.widget_central)
        self.show()

        # Conectar los botones a sus respectivas funciones
        self.botones_widget.children()[1].clicked.connect(self.mostrar_palabra)
        self.botones_widget.children()[3].clicked.connect(self.mostrar_dimensiones)

    def mostrar_palabra(self):
        # Obtener el texto ingresado en la QLineEdit
        palabra = self.palabra_ingresada.text()
        # Actualizar la descripción de los botones con la palabra ingresada
        self.descripcion_botones.setText(palabra)

    def mostrar_dimensiones(self):
        # Obtener las dimensiones actuales de la ventana
        width = self.width()
        height = self.height()
        # Actualizar la descripción con las dimensiones actuales
        self.descripcion_botones.setText(f"Dimensiones actuales de la ventana: {width}x{height}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
