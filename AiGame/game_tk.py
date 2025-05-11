import cv2 
import mediapipe as mp
import random
import tkinter as tk
from PIL import Image, ImageTk

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

player_move = ""
ai_move = ""
last_player_move = ""
result_text = ""

def get_hand_move(landmarks):
    finger_states = [landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20]]
    if all(finger_states):
        return "Paper"
    elif not any(finger_states):
        return "Rock"
    elif finger_states[0] and finger_states[1] and not any(finger_states[2:]):
        return "Scissors"
    return "Unknown"

def get_ai_move():
    return random.choice(["Rock", "Paper", "Scissors"])

def determine_winner():
    global player_move, ai_move
    if player_move == ai_move:
        return "Draw"
    elif (player_move == "Rock" and ai_move == "Scissors") or \
         (player_move == "Scissors" and ai_move == "Paper") or \
         (player_move == "Paper" and ai_move == "Rock"):
        return "Player Wins!"
    else:
        return "AI Wins!"

def update_game():
    global player_move, ai_move, last_player_move, result_text
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            player_move = get_hand_move(hand_landmarks.landmark)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        player_move = ""
        last_player_move = ""
    
    if player_move and player_move != last_player_move:
        ai_move = get_ai_move()
        last_player_move = player_move
        result_text = determine_winner()

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = ImageTk.PhotoImage(img)
    video_label.config(image=img)
    video_label.image = img
    
    player_label.config(text=f"Player: {player_move}")
    ai_label.config(text=f"AI: {ai_move}")
    result_label.config(text=result_text)
    
    root.after(50, update_game)

root = tk.Tk()
root.title("AI Rock-Paper-Scissors")
root.geometry("800x600")

video_label = tk.Label(root)
video_label.pack()

player_label = tk.Label(root, text="Player: ", font=("Arial", 16))
player_label.pack()
ai_label = tk.Label(root, text="AI: ", font=("Arial", 16))
ai_label.pack()
result_label = tk.Label(root, text="", font=("Arial", 18, "bold"))
result_label.pack()

cap = cv2.VideoCapture(0)
update_game()  

root.mainloop()
