import numpy as np
import torch
from collections import deque
import socketio
import time
from semg_model import SEMGCNN, WINDOW_SIZE
import joblib

# Load label encoder and model
le = joblib.load("label_encoder_cnn.pkl")
n_classes = len(le.classes_)
model = SEMGCNN(n_classes=n_classes)
model.load_state_dict(torch.load("semg_cnn.pth", map_location="cpu"))
model.eval()

# Initialize buffer
buffer = deque(maxlen=WINDOW_SIZE)

def process_and_predict(data):
    try:
        raw = np.array(
            [
                data["ch0"]["a"],
                # data["ch0"]["e"],
                data["ch1"]["a"],
                # data["ch1"]["e"],
                data["ch2"]["a"],
                # data["ch2"]["e"],
                data["ch3"]["a"],
                # data["ch3"]["e"],
            ]
        )
        buffer.append(raw)
        if len(buffer) == WINDOW_SIZE:
            window = np.stack(buffer, axis=1)

            # Normalize per channel
            norm_signal = (window - window.mean(axis=1, keepdims=True)) / (window.std(axis=1, keepdims=True) + 1e-6)
            tensor = torch.tensor(norm_signal, dtype=torch.float32).unsqueeze(0)  # (1, 2, 600)

            with torch.no_grad():
                out = model(tensor)
                pred = out.argmax(dim=1).item()
                buffer.clear()
                return le.inverse_transform([pred])[0]
    except Exception as e:
        print(f"Inference error: {e}")
    return None

# SocketIO setup
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to Socket.IO server.")

@sio.on("adc_data")
def semg_data(data):
    prediction = process_and_predict(data)
    if prediction:
        print(f"Detection: {prediction}")

if __name__ == "__main__":
    sio.connect("http://localhost:3000", transports=["websocket"], namespaces=["/"])
    try:
        print("waiting...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sio.disconnect()
