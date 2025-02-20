import cv2
import mediapipe as mp
import numpy as np
import csv
import os


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define labels for sign gestures
GESTURES = ["hello", "yes", "no", "thanks", "stop"]
DATA_FILE = "sign_data.csv"

# Create CSV file for dataset if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)])


def collect_data():
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        for gesture in GESTURES:
            print(f"📸 Collecting data for: {gesture}. Press 's' to start recording, 'q' to quit.")
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw hand landmarks
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                cv2.putText(image, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Collecting Sign Data", image)

                key = cv2.waitKey(1)
                if key == ord('s'):
                    print(f"✏️ Recording data for {gesture}...")
                    for _ in range(100):  # Collect 100 samples per gesture
                        ret, frame = cap.read()
                        if not ret:
                            break

                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        results = hands.process(image)

                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                landmark_list = []
                                for landmark in hand_landmarks.landmark:
                                    landmark_list.append(landmark.x)
                                    landmark_list.append(landmark.y)

                                # Save landmark data to CSV
                                with open(DATA_FILE, "a", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow([gesture] + landmark_list)

                elif key == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    collect_data()
