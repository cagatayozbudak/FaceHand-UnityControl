import cv2
import mediapipe as mp
import numpy as np
import socket

# Initialize MediaPipe Face Mesh (for face tracking)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Initialize MediaPipe Hands (for hand tracking)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set up UDP connection to Unity
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UNITY_IP = "127.0.0.1"   # Localhost (same computer)
UNITY_PORT = 5052        # Port Unity is listening on

# Start the webcam
cap = cv2.VideoCapture(0)

# Store the reference face size (used for forward/backward movement)
reference_face_size = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image horizontally (mirror effect)
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face and hands
    results_face = face_mesh.process(rgb_frame)
    results_hands = hands.process(rgb_frame)

    # Default movement and rotation values
    move_x, move_y, move_z = 0, 0, 0
    rotate_y = 0  # Rotation from hand gesture (Y axis)

    # --- FACE TRACKING: Move in X, Y, Z directions ---
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            # Get nose position (used as main tracking point)
            nose_x = face_landmarks.landmark[1].x * w
            nose_y = face_landmarks.landmark[1].y * h

            # Compare with screen center
            center_x, center_y = w // 2, h // 2

            move_x = (nose_x - center_x) / center_x * 5    # Left/Right movement
            move_y = (nose_y - center_y) / center_y * 5    # Up/Down movement

            # Draw a bounding box around the face
            x_min = int(min([lm.x * w for lm in face_landmarks.landmark]))
            y_min = int(min([lm.y * h for lm in face_landmarks.landmark]))
            x_max = int(max([lm.x * w for lm in face_landmarks.landmark]))
            y_max = int(max([lm.y * h for lm in face_landmarks.landmark]))
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Estimate forward/backward movement based on face size
            face_size = x_max - x_min
            if reference_face_size is None:
                reference_face_size = face_size

            move_z = ((face_size - reference_face_size) / reference_face_size) * 5
            move_z *= -1  # Invert: positive = forward

            # Draw a green dot on the nose (tracking point)
            cv2.circle(frame, (int(nose_x), int(nose_y)), 5, (0, 255, 0), -1)

    # --- HAND TRACKING: Rotate Left/Right ---
    if results_hands.multi_hand_landmarks and len(results_hands.multi_hand_landmarks) == 1:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            hand_x = hand_landmarks.landmark[9].x * w  # Approx center of hand

            # Decide rotation based on hand position
            if hand_x < w / 3:
                rotate_y = -10  # Rotate left
            elif hand_x > 2 * w / 3:
                rotate_y = 10   # Rotate right

    # Draw a red dot in the center of the screen
    cv2.circle(frame, (w // 2, h // 2), 5, (0, 0, 255), -1)

    # Send data to Unity: moveX, moveY, moveZ, rotateY
    data = f"{move_x},{move_y},{move_z},{rotate_y}"
    sock.sendto(data.encode(), (UNITY_IP, UNITY_PORT))

    # Show the camera preview with tracking overlays
    cv2.imshow("Face & Hand Tracking (Unity Control)", frame)

    # Press 'Esc' to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()