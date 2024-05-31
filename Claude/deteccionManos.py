import cv2
import mediapipe as mp

# Inicializar el detector de manos de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Abrir la cámara
cap = cv2.VideoCapture(0)

while True:
    # Leer un fotograma del video
    ret, frame = cap.read()

    # Convertir a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar el fotograma para detectar manos
    results = hands.process(rgb_frame)

    # Dibujar los puntos de referencia de las manos detectadas
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostrar el fotograma resultante
    cv2.imshow('Hand Detection', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()