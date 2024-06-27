import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QTimer
import cv2

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("border: 5px solid gray; border-radius: 15px;")
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addStretch(1)  # Añadir espacio elástico para centrar verticalmente
        self.setLayout(layout)

        self.capture = None
        self.timer = QTimer()

    def start_camera(self):
        """
        Función para iniciar la captura de la cámara desde el botón.
        """
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)

    def stop_camera(self):
        """
        Función para detener la captura de la cámara.
        """
        if self.capture and self.capture.isOpened():
            self.timer.stop()
            self.capture.release()
            self.capture = None
            self.camera_label.clear()  # Limpiar el contenido del QLabel al detener la cámara

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.camera_label.setPixmap(pixmap)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interfaz Gráfica con PyQt5')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #e0f2f1;")  # Color de fondo azul claro

        # Botones con esquinas redondeadas y colores pasteles
        btn_capturar = QPushButton('Capturar Muestras')
        btn_capturar.setStyleSheet(
            "QPushButton { background-color: #ffd1dc; border: 2px solid #e6b8ca; "
            "border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #ffb6c1; }"
        )
        btn_capturar.clicked.connect(self.start_camera)  # Conectar el botón a la función start_camera

        btn_detener = QPushButton('Detener Cámara')
        btn_detener.setStyleSheet(
            "QPushButton { background-color: #ff9999; border: 2px solid #e67373; "
            "border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #ff6666; }"
        )
        btn_detener.clicked.connect(self.stop_camera)  # Conectar el botón a la función stop_camera

        btn_crear_puntos = QPushButton('Crear Puntos Característicos')
        btn_crear_puntos.setStyleSheet(
            "QPushButton { background-color: #bdfcc9; border: 2px solid #a3e9b3; "
            "border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #a1e9bd; }"
        )

        btn_entrenar_modelo = QPushButton('Entrenar Modelo')
        btn_entrenar_modelo.setStyleSheet(
            "QPushButton { background-color: #ffe5b4; border: 2px solid #ffd699; "
            "border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #ffd188; }"
        )

        btn_evaluar_modelo = QPushButton('Evaluar Modelo')
        btn_evaluar_modelo.setStyleSheet(
            "QPushButton { background-color: #b3e0ff; border: 2px solid #8fc5e0; "
            "border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #99d1ff; }"
        )

        # Espacio para ingresar texto
        self.txt_palabra = QLineEdit()
        self.txt_palabra.setStyleSheet(
            "QLineEdit { border: 2px solid #b3b3b3; border-radius: 10px; padding: 8px; font-size: 16px; }"
            "QLineEdit:focus { border-color: #0071D5; }"
        )

        # Widget de la cámara
        self.camera_widget = CameraWidget()

        # Layout principal
        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.camera_widget, alignment=Qt.AlignCenter)  # Alineación centrada horizontalmente
        vbox_main.addWidget(self.txt_palabra)
        
        # Layout para los botones
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(btn_capturar)
        hbox_buttons.addWidget(btn_detener)
        hbox_buttons.addWidget(btn_crear_puntos)
        hbox_buttons.addWidget(btn_entrenar_modelo)
        hbox_buttons.addWidget(btn_evaluar_modelo)
        vbox_main.addLayout(hbox_buttons)

        self.setLayout(vbox_main)

    def start_camera(self):
        """
        Función para iniciar la captura de la cámara desde el botón.
        """
        self.camera_widget.start_camera()

    def stop_camera(self):
        """
        Función para detener la captura de la cámara desde el botón.
        """
        self.camera_widget.stop_camera()

    def closeEvent(self, event):
        """
        Función para manejar el evento de cierre de la ventana principal.
        """
        self.camera_widget.stop_camera()  # Detener la cámara al cerrar la ventana

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
