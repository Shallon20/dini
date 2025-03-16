import cv2
import mediapipe as mp
import numpy as np
import csv
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Path to store collected data
DATA_FILE = "sign_data.csv"

# Create CSV file if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)])


def collect_data(label):
    """Capture hand landmarks from webcam and save to CSV with a label."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not access the webcam!")
        return

    print(f"Collecting data for: {label}. Press 'q' to stop recording.")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract x, y coordinates of 21 landmarks (42 features)
                landmark_data = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark]).flatten()

                # Save to CSV
                with open(DATA_FILE, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([label] + list(landmark_data))

                frame_count += 1
                print(f"Frame {frame_count} saved for {label}")

        # Show webcam feed
        cv2.putText(frame, f"Recording: {label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Collecting Data", frame)

        # Press 'q' to stop collecting data
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Data collection for '{label}' finished.")


# Run the script
if __name__ == "__main__":
    label = input("Enter the label for this sign: ")
    collect_data(label)
