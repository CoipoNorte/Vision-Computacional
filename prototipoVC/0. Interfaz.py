import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from tensorflow.keras.models import load_model
from mediapipe.python.solutions.holistic import Holistic
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from text_to_speech import text_to_speech

# Parámetros y configuraciones
MAX_LENGTH_FRAMES = 15
MIN_LENGTH_FRAMES = 5
ROOT_PATH = os.getcwd()
DATA_PATH = os.path.join(ROOT_PATH, "data")
MODELS_PATH = os.path.join(ROOT_PATH, "models")
MODEL_NAME = f"actions_{MAX_LENGTH_FRAMES}.keras"
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 1.5

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def there_hand(results):
    return results.left_hand_landmarks or results.right_hand_landmarks

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
    return np.concatenate([pose, face, lh, rh])

def get_actions(path):
    out = []
    for action in os.listdir(path):
        name, ext = os.path.splitext(action)
        if ext == ".h5":
            out.append(name)
    return out

class EvaluarModeloApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = load_model(os.path.join(MODELS_PATH, MODEL_NAME))
        self.holistic_model = Holistic()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.video_capture = cv2.VideoCapture(0)
        self.kp_sequence = []
        self.sentence = []
        self.count_frame = 0

    def initUI(self):
        self.setWindowTitle('Traductor LSCH - Prototipo VC')
        self.setGeometry(100, 100, 800, 600)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        
        self.translation_label = QLabel("Traducción: ", self)
        self.translation_label.setStyleSheet("font-size: 16px; color: black; background-color: white; padding: 10px; border-radius: 10px;")
        self.layout.addWidget(self.translation_label)
        
        self.btn_evaluar = QPushButton('Evaluar Modelo', self)
        self.btn_evaluar.setStyleSheet("background-color: #1CA5B8; color: white; border-radius: 10px; padding: 10px;")
        self.btn_evaluar.clicked.connect(self.start_evaluation)
        self.layout.addWidget(self.btn_evaluar)
        
        self.setLayout(self.layout)

    def start_evaluation(self):
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return
        
        image, results = mediapipe_detection(frame, self.holistic_model)
        self.kp_sequence.append(extract_keypoints(results))

        if len(self.kp_sequence) > MAX_LENGTH_FRAMES and there_hand(results):
            self.count_frame += 1
        else:
            if self.count_frame >= MIN_LENGTH_FRAMES:
                res = self.model.predict(np.expand_dims(self.kp_sequence[-MAX_LENGTH_FRAMES:], axis=0))[0]
                if res[np.argmax(res)] > 0.7:
                    sent = get_actions(DATA_PATH)[np.argmax(res)]
                    self.sentence.insert(0, sent)
                    self.translation_label.setText(f"Traducción: {sent}")
                    text_to_speech(sent)
                self.count_frame = 0
                self.kp_sequence = []

        if self.sentence:
            cv2.putText(image, self.sentence[0], (10, image.shape[0] - 10), FONT, FONT_SIZE, (0, 0, 0), 2)

        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(qimage))

    def closeEvent(self, event):
        self.timer.stop()
        self.video_capture.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = EvaluarModeloApp()
    window.show()
    app.exec_()
