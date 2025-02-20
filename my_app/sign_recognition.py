import os
# Force TensorFlow to use GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
from collections import deque
from django.http import JsonResponse

# Load trained model
model = tf.keras.models.load_model("sign_model.h5")

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Queue for storing recognized words
sentence_queue = deque(maxlen=10)  # Store last 10 words for fluid translation

def process_frame(frame):
    """Process a single frame for hand landmarks and predict sign language."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        image_height, image_width, _ = frame.shape
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract hand landmark coordinates (x, y only) → 21 landmarks * 2 = 42 features
            landmark_data = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark]).flatten().reshape(1, -1)

            # Ensure correct shape for prediction
            print(f"Input Shape for Prediction: {landmark_data.shape}")  # Debugging

            if landmark_data.shape[1] != 42:
                print(f"⚠️ ERROR: Incorrect input shape {landmark_data.shape}. Expected (1, 42).")
                return ""

            # Predict sign
            prediction = model.predict(landmark_data)
            predicted_label = np.argmax(prediction)

            # Convert label to text (adjust based on your dataset)
            label_map = {0: "hello", 1: "yes", 2: "no", 3: "thank you", 4: "please"}
            word = label_map.get(predicted_label, "")

            if word:
                sentence_queue.append(word)  # Add word to sentence queue

    return " ".join(sentence_queue)  # Return continuous sentence

# Start real-time sign recognition
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # Get translated sentence
        translated_text = process_frame(frame)

        # Display result on OpenCV window
        cv2.putText(frame, translated_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Sign Language Translator", frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
