import cv2
import mediapipe as mp
import os

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# ---------------------- Static Image Processing ----------------------
def process_static_image(image_path):
    """Processes a single image for hand landmarks."""
    if not os.path.exists(image_path):
        print("⚠️ Image not found!")
        return None

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)  # Flip for correct orientation
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(
        static_image_mode=True,  # Static mode enabled
        max_num_hands=2,
        min_detection_confidence=0.5
    ) as hands:
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        cv2.imshow("Processed Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ---------------------- Live Webcam Processing ----------------------
def process_webcam():
    """Processes real-time webcam input for hand landmarks."""
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("⚠️ Ignoring empty camera frame.")
                continue

            # Convert the image to RGB for processing
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Convert back to BGR for OpenCV display
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw landmarks if detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

            # Flip image for selfie-view
            cv2.imshow("AI Sign Recognition", cv2.flip(image, 1))

            if cv2.waitKey(5) & 0xFF == 27:  # Press "Esc" to exit
                break

    cap.release()
    cv2.destroyAllWindows()

# ---------------------- Run Mode Selection ----------------------
if __name__ == "__main__":
    mode = input("Enter 'live' for webcam or 'image' for static image processing: ")

    if mode == "live":
        print("🎥 Starting Live Webcam Mode...")
        process_webcam()
    elif mode == "image":
        image_path = input("Enter the image path: ")
        print(f"📸 Processing Image: {image_path} ...")
        process_static_image(image_path)
    else:
        print("⚠️ Invalid option. Please enter 'live' or 'image'.")
