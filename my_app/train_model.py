# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout
#
# # Load Dataset
# DATA_FILE = "sign_data.csv"
# df = pd.read_csv(DATA_FILE)
#
# # Prepare Data
# X = df.drop(columns=["label"]).values  # Landmark coordinates
# y = pd.get_dummies(df["label"]).values  # Convert labels to one-hot encoding
#
# # Split Dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # Build Model
# model = Sequential([
#     Dense(128, activation="relu", input_shape=(X.shape[1],)),
#     Dropout(0.3),
#     Dense(64, activation="relu"),
#     Dense(len(y[0]), activation="softmax")  # Output layer with softmax activation
# ])
#
# # Compile Model
# model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
#
# # Train Model
# model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))
#
# # Save Model
# model.save("sign_model.h5")
# print("Model saved as sign_model.h5")

import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
import cv2



# Limit TensorFlow memory usage
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
# Define correct paths inside Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root
DATA_FILE = os.path.join(BASE_DIR, "my_app/media-csv/dataset/Train.csv")
IMAGE_FOLDER = os.path.join(BASE_DIR, "my_app/static/img/dataset-imgs/Images/")

# Load Dataset
df = pd.read_csv(DATA_FILE)

# Function to load images
def load_images(image_ids, image_folder):
    images = []
    for img_id in image_ids:
        img_path = os.path.join(image_folder, img_id + ".jpg")  # Assuming .jpg images
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            img = cv2.resize(img, (64, 64))
            img = img / 255.0  # Normalize
            images.append(img)
        else:
            print(f"WARNING: {img_path} not found!")
            images.append(np.zeros((128, 128, 3)))  # Placeholder
    return np.array(images)

# Load images and labels
X = load_images(df["img_IDS"], IMAGE_FOLDER)
y = pd.factorize(df["Label"])[0]  # Convert labels to numerical values

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(len(set(y)), activation="softmax")  # Output layer
])

# Compile Model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train Model
model.fit(X_train, y_train, epochs=5, batch_size=4, validation_data=(X_test, y_test))

# Save Model inside Django static folder
model_path = os.path.join(BASE_DIR, "my_app/static/model/sign_model.h5")
model.save(model_path)
print(f"Model saved at {model_path}")
