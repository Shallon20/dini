import os
import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
from collections import deque
from django.http import JsonResponse

# force TensorFlow to use GPU if available
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Load trained model
model = tf.keras.models.load_model("sign_model.h5")

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Sentence storaaage for continuous translation
sentence_queue = deque(maxlen=10)  # Store last 10 words

def process_frame(frame):
    """Process a single frame for hand landmarks and predict sign language."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract x, y coordinates of 21 landmarks(42 features)
            landmark_data = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark]).flatten().reshape(1, -1)

            # Ensure input shape matches model expectation
            if landmark_data.shape[1] != 42:
                print(f" ERROR: Incorrect input shape {landmark_data.shape}. Expected (1, 42).")
                return ""

            # Predict sign
            prediction = model.predict(landmark_data)
            predicted_label = np.argmax(prediction)

            # Convert label to text (update based on trained dataset)
            label_map = {0: "hello", 1: "yes", 2: "no", 3: "thank you", 4: "please"}
            word = label_map.get(predicted_label, "")

            if word:
                sentence_queue.append(word)  # store recognized words

    return " ".join(sentence_queue)  # Return translated sentence

