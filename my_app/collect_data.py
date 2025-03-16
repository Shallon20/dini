import cv2
import mediapipe as mp
import numpy as np
import csv
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define labels for sign gestures
DATA_FILE = "sign_data.csv"

# Create CSV file for dataset if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)])


def collect_data(label):
    """Collect hand landmarks from webcam and save to CSV"""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return

    frame_skip = 5  # Capture every 5th frame
    frame_count = 0  # Track processed frames

    with mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # **Check for 'q' Key Press to Stop**
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopping data collection...")
                break

            # **Display the Camera Feed**
            cv2.imshow("Collecting Data - Press 'q' to Stop", frame)

            # Skip frames to avoid redundancy
            if frame_count % frame_skip != 0:
                frame_count += 1
                continue

            # Convert image to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            # Extract hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmark_list = []
                    for landmark in hand_landmarks.landmark:
                        landmark_list.append([landmark.x])
                        landmark_list.append([landmark.y])

                    # Save original data
                    with open(DATA_FILE, "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([label] + [coord for landmark in landmark_list for coord in landmark])

                    print(f"Saved frame {frame_count}")

            # **FLIP FRAME FOR DATA AUGMENTATION**
            flipped_frame = cv2.flip(frame, 1)  # Flip image horizontally
            image_rgb_flipped = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
            results_flipped = hands.process(image_rgb_flipped)

            if results_flipped.multi_hand_landmarks:
                for hand_landmarks in results_flipped.multi_hand_landmarks:
                    landmark_list = []
                    for landmark in hand_landmarks.landmark:
                        landmark_list.append([landmark.x])
                        landmark_list.append([landmark.y])

                    # Save flipped data with SAME label
                    with open(DATA_FILE, "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([label] + [coord for landmark in landmark_list for coord in landmark])

                    print(f"Saved FLIPPED frame {frame_count}")

            frame_count += 1

    cap.release()
    cv2.destroyAllWindows()  # Close all OpenCV windows
    print(f"Data collection for '{label}' completed.")


if __name__ == "__main__":
    label = input("Enter the label for this sign: ")
    print(f"Collecting data for: {label}. Press 'q' to stop recording.")
    collect_data(label)
