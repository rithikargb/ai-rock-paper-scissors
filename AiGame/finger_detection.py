import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmark_list = []
            h, w, c = frame.shape
            for idx, landmark in enumerate(hand_landmarks.landmark):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmark_list.append((idx, cx, cy))

            if landmark_list:
                fingers = []

                if landmark_list[4][1] > landmark_list[2][1]:  
                    fingers.append(1)
                else:
                    fingers.append(0)

                for tip, lower in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    if landmark_list[tip][2] < landmark_list[lower][2]:  
                        fingers.append(1)
                    else:
                        fingers.append(0)

                print(f"Fingers: {fingers}")

    cv2.imshow("Finger Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
