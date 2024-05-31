import cv2
import mediapipe as mp

# Inicializar el detector de pose de MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Abrir la cámara
cap = cv2.VideoCapture(0)

while True:
    # Leer un fotograma del video
    ret, frame = cap.read()

    # Convertir a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar el fotograma para detectar la pose
    results = pose.process(rgb_frame)

    # Dibujar los puntos de referencia de la pose detectada
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Mostrar el fotograma resultante
    cv2.imshow('Pose Detection', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()