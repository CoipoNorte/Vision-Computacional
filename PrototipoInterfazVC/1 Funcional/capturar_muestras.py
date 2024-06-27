# capturar_muestras.py
import os
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from mediapipe.python.solutions.holistic import Holistic
from mediapipe.python.solutions.holistic import FACEMESH_CONTOURS, POSE_CONNECTIONS, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks, DrawingSpec
from typing import NamedTuple

# Define the word to capture samples for
PALABRA = "CoipoNorte"

# Image parameters
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 1.5
FONT_POS = (5, 30)

# Create a folder if it does not exist
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Perform mediapipe detection
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

# Check if there's a hand in the frame
def there_hand(results: NamedTuple) -> bool:
    return results.left_hand_landmarks or results.right_hand_landmarks

# Save frames to disk
def save_frames(frames, output_folder):
    for num_frame, frame in enumerate(frames):
        frame_path = os.path.join(output_folder, f"{num_frame + 1}.jpg")
        cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA))

# Draw keypoints on the image
def draw_keypoints(image, results):
    # Draw facial landmarks
    draw_landmarks(
        image,
        results.face_landmarks,
        FACEMESH_CONTOURS,
        DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),  # Red for facial landmarks
        DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),  # Yellow for contours
    )

    # Draw pose landmarks
    draw_landmarks(
        image,
        results.pose_landmarks,
        POSE_CONNECTIONS,
        DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),  # Green for pose
        DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),  # Blue for pose (contrast)
    )

    # Draw left hand landmarks
    draw_landmarks(
        image,
        results.left_hand_landmarks,
        HAND_CONNECTIONS,
        DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),  # Green for left hand
        DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),  # Blue for left hand connections
    )

    # Draw right hand landmarks
    draw_landmarks(
        image,
        results.right_hand_landmarks,
        HAND_CONNECTIONS,
        DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),  # Red for right hand
        DrawingSpec(color=(255, 165, 0), thickness=2, circle_radius=2),  # Orange for right hand connections
    )

# Capture samples with the given word and update the widget
def capturar_muestras(path, camera_widget, margin_frame=2, min_cant_frames=5):
    create_folder(path)
    cant_sample_exist = len(os.listdir(path))

    count_sample = 0
    count_frame = 0
    frames = []

    with Holistic() as holistic_model:
        video = cv2.VideoCapture(0)

        while video.isOpened():
            _, frame = video.read()
            image, results = mediapipe_detection(frame, holistic_model)

            if there_hand(results):
                count_frame += 1
                if count_frame > margin_frame:
                    cv2.putText(image, 'GRABANDO', FONT_POS, FONT, FONT_SIZE, (0, 0, 255))
                    frames.append(np.asarray(frame))
            else:
                if len(frames) > min_cant_frames + margin_frame:
                    frames = frames[:-margin_frame]
                    output_folder = os.path.join(path, f"sample_{cant_sample_exist + count_sample + 1}")
                    create_folder(output_folder)
                    save_frames(frames, output_folder)
                    count_sample += 1

                frames = []
                count_frame = 0
                cv2.putText(image, 'Buscando Manos...', FONT_POS, FONT, FONT_SIZE, (0, 255, 0))

            draw_keypoints(image, results)

            # Update the camera widget
            if camera_widget:
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                camera_widget.setPixmap(pixmap)

            if cv2.waitKey(10) & 0xFF == ord('c'):
                break

        video.release()

def main(word_name, camera_widget=None):
    ROOT_PATH = os.getcwd()
    FRAME_ACTIONS_PATH = os.path.join(ROOT_PATH, "frame_actions")
    word_path = os.path.join(FRAME_ACTIONS_PATH, word_name)

    capturar_muestras(word_path, camera_widget)

if __name__ == "__main__":
    import sys

    word_name = sys.argv[1] if len(sys.argv) > 1 else PALABRA

    main(word_name)
