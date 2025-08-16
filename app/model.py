import base64

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sqlmodel import Session

from app.database import engine
from app.schemas import ModelData

data = pd.read_csv("./data/weather_classification_data.csv")

label_encoders = {}
categorical_cols = ["Cloud Cover", "Season", "Location", "Weather Type"]
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

X = data.drop("Weather Type", axis=1)
y = data["Weather Type"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
numerical_cols = [
    "Temperature",
    "Humidity",
    "Wind Speed",
    "Precipitation (%)",
    "Atmospheric Pressure",
    "UV Index",
    "Visibility (km)",
]
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

num_classes = len(label_encoders["Weather Type"].classes_)

model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=50,
    batch_size=32,
    verbose=1,
)


def predict_weather(input_data):
    input_df = pd.DataFrame([input_data])

    for col in ["Cloud Cover", "Season", "Location"]:
        if col in input_df.columns:
            le = label_encoders[col]
            input_df[col] = le.transform([input_data[col]])[0]

    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

    prediction = model.predict(input_df)
    predicted_class = np.argmax(prediction, axis=1)[0]

    weather_type = label_encoders["Weather Type"].inverse_transform([predicted_class])[
        0
    ]

    return weather_type


converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

size = len(tflite_model)
base64_model = base64.b64encode(tflite_model).decode("utf-8")

with Session(engine) as session:
    nn = ModelData(data=base64_model, size=size)
    session.add(nn)
    session.commit()
    session.refresh(nn)
