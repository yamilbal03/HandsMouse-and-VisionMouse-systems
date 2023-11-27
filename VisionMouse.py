import cv2
import mediapipe as mp
import pyautogui
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Lista para almacenar las últimas posiciones del mouse
previous_mouse_positions = []

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y

                # Suavizado del movimiento vertical
                smooth_factor =0.375  # Ajusta este valor para el suavizado
                if len(previous_mouse_positions) > 0:
                    prev_x, prev_y = previous_mouse_positions[-1]
                    smooth_x = int((1 - smooth_factor) * prev_x + smooth_factor * screen_x)
                    smooth_y = int((1 - smooth_factor) * prev_y + smooth_factor * screen_y)
                    pyautogui.moveTo(smooth_x, smooth_y )
                    previous_mouse_positions.append((smooth_x, smooth_y))
                else:
                    pyautogui.moveTo(screen_x, screen_y )
                    previous_mouse_positions.append((screen_x, screen_y))

                # Limita el tamaño de la lista de posiciones anteriores para el suavizado
                if len(previous_mouse_positions) > 10:
                    previous_mouse_positions.pop(0)

        left = [landmarks[145], landmarks[159]]
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
    cv2.imshow('Eye Controlled Mouse', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.VideoCapture(0).release()
cv2.destroyAllWindows()
