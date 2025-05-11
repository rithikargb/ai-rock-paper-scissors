import cv2
import mediapipe as mp
import random

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

ai_move = random.choice(["Rock", "Paper", "Scissors"])
last_player_move = None

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.2
font_thickness = 3
text_color = (255, 255, 255)
outline_color = (0, 0, 0)

def draw_text(frame, text, position, color=text_color):
    x, y = position
    cv2.putText(frame, text, (x+2, y+2), font, font_scale, outline_color, font_thickness+2, cv2.LINE_AA)
    cv2.putText(frame, text, (x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)

while True:
    success, frame = cap.read()
    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    player_move = "None"

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

                if fingers == [0, 0, 0, 0, 0]:
                    player_move = "Rock"
                elif sum(fingers) >= 4:
                    player_move = "Paper"
                elif fingers == [0, 1, 1, 0, 0]:
                    player_move = "Scissors"

    if player_move != "None" and player_move != last_player_move:
        ai_move = random.choice(["Rock", "Paper", "Scissors"])
        last_player_move = player_move

    if player_move == ai_move:
        result = "Draw!"
    elif (player_move == "Rock" and ai_move == "Scissors") or \
         (player_move == "Paper" and ai_move == "Rock") or \
         (player_move == "Scissors" and ai_move == "Paper"):
        result = "You Win!"
    else:
        result = "AI Wins!"

    if result == "You Win!":
        result_color = (0, 255, 0)
    elif result == "AI Wins!":
        result_color = (0, 0, 255)
    else:
        result_color = (255, 255, 0)

    draw_text(frame, f"Player: {player_move}", (50, 50), (0, 255, 0))
    draw_text(frame, f"AI: {ai_move}", (50, 100), (0, 255, 255))
    draw_text(frame, result, (50, 160), result_color)

    cv2.imshow("Rock Paper Scissors - AI Game", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
