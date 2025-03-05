import os
import sys

import pandas as pd
import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
from collections import deque
from django.http import JsonResponse

# force TensorFlow to use GPU if available
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Get the model path dynamically
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sign_model.h5"))
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sign_data.csv"))

# Load label names dynamically from training data
def load_labels():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        unique_labels = sorted(df["label"].unique())
        return {i: label for i, label in enumerate(unique_labels)}
    return {}

label_map = load_labels()  # Get dynamic labels from dataset


# Load model only if it exists
if os.path.exists(MODEL_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    except Exception as e:
        print(f"ERROR: Unable to load model: {e}")
        model = None  # Prevent crashing
else:
    print("ERROR: sign_model.h5 not found!")
    model = None  # Prevent crashing

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Sentence storage for continuous translation
sentence_queue = deque(maxlen=1)  # Store last 10 words

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

            # Convert label to text dynamically
            word = label_map.get(predicted_label, "")

            if word:
                sentence_queue.append(word)  # store recognized words

    return " ".join(sentence_queue)  # Return translated sentence

