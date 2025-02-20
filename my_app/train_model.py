import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Load Dataset
df = pd.read_csv("sign_data.csv")

# Prepare Data
X = df.drop(columns=["label"]).values  # Feature Data (Landmarks)
y = pd.get_dummies(df["label"]).values  # One-hot encoded Labels

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build Model
model = Sequential([
    Dense(128, activation="relu", input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(64, activation="relu"),
    Dense(len(y[0]), activation="softmax")  # Output layer with softmax for classification
])

# Compile Model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train Model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Save Model
model.save("sign_model.h5")
print("✅ Model saved as sign_model.h5")
