import cv2
import mediapipe as mp

# Inicializar los detectores de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

# Crear instancia del detector holístico
holistic = mp_holistic.Holistic(static_image_mode=False, model_complexity=2, enable_segmentation=True)

# Crear instancia de los detectores de rostro y pose
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True)

# Abrir la cámara
cap = cv2.VideoCapture(0)

while True:
    # Leer un fotograma del video
    ret, frame = cap.read()

    # Convertir a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar el fotograma para detectar rostro, manos y cuerpo
    results = holistic.process(rgb_frame)
    face_mesh_results = face_mesh.process(rgb_frame)
    pose_results = pose.process(rgb_frame)

    # Dibujar los puntos de referencia detectados
    mp_drawing.draw_landmarks(frame, face_mesh_results.multi_face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Mostrar el fotograma resultante
    cv2.imshow('Holistic Detection', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()