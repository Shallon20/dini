# import cv2
# import mediapipe as mp
# import numpy as np
# import csv
# import os
#
# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
#
# # Define labels for sign gestures
# file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads"))
#
# DATA_FILE = "sign_data.csv"
#
# # Create CSV file for dataset if not exists
# if not os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "w", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow(["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)])
#
#
# def process_uploaded_file(filepath, label):
#     """Extract hand landmarks from an uploaded video/image and save to CSV"""
#     full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads", os.path.basename(filepath)))
#     print(f"Checking file path: {os.path.abspath(full_path)}") # debugging
#     cap = cv2.VideoCapture(full_path)
#     if not cap.isOpened():
#         print(f"ERROR: Could not open video file {filepath}")
#         return
#
#     with mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5) as hands:
#         frame_count = 0  # Track number of processed frames
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#
#             # Convert image to RGB
#             image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = hands.process(image_rgb)
#
#             # Extract hand landmarks
#             if results.multi_hand_landmarks:
#                 frame_count += 1  # Count frames with detected hands
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     landmark_list = []
#                     for landmark in hand_landmarks.landmark:
#                         landmark_list.append([landmark.x])
#                         landmark_list.append([landmark.y])
#                     print(f"Saving frame {frame_count} from {filepath}")  # Debugging output
#                     # Save data to CSV
#                     with open(DATA_FILE, "a", newline="") as file:
#                         writer = csv.writer(file)
#                         writer.writerow([label] + [coord for landmark in landmark_list for coord in landmark])
#         print(f"{frame_count} frames processed from {filepath}")
#     cap.release()
#
#
# if __name__ == "__main__":
#     print("Place your vidoes/images in 'uploads/ folder and run this script")
#     UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
#     for filename in os.listdir(UPLOAD_FOLDER):
#         if filename.endswith((".mp4", ".jpg", "png")):
#             label = input(f"Enter label for {filename}: ")
#             process_uploaded_file(os.path.join("uploads/", filename), label)
#             print(f"Processed {filename}")
#         if not os.path.exists(UPLOAD_FOLDER):
#             print("ERROR: 'uploads/' folder does not exist! Creating it now...")
#             os.makedirs(UPLOAD_FOLDER)



import os
import cv2
import numpy as np
import pandas as pd
import csv
from django.core.files.storage import default_storage

# Define paths inside Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_FOLDER = os.path.join(BASE_DIR, "my_app/static/img/dataset-imgs/Images/")
DATA_FILE = os.path.join(BASE_DIR, "my_app/media-csv/dataset/Train.csv")

# Ensure directories exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# Create CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["img_IDS", "Label"])  # Header row

def save_uploaded_image(uploaded_file, label):
    """Save an uploaded image and update Train.csv"""
    # Get the image filename
    image_filename = uploaded_file.name

    # Save the image to the images folder
    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    with open(image_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # Update the Train.csv file
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([image_filename.split(".")[0], label])  # Store ID without extension

    return f"Image {image_filename} saved successfully with label {label}!"

# Example: Simulating an upload (For testing)
if __name__ == "__main__":
    test_image_path = os.path.join(BASE_DIR, "test_image.jpg")  # Replace with an actual image path
    test_label = "Friend"

    if os.path.exists(test_image_path):
        with open(test_image_path, "rb") as img:
            print(save_uploaded_image(img, test_label))
    else:
        print("Test image not found. Please upload an image.")
