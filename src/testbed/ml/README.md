
# Real-Time sEMG Classification System

This project implements a complete machine learning pipeline for the classification of surface electromyography (sEMG) signals in real-time using a neural network model. It is designed to process signals from two sEMG channels and detect physical actions or gestures based on envelope and activation levels. The system reads training data from a CSV file and performs real-time inference using WebSocket streaming.

---

## 📁 Dataset

The dataset used is in `combined.csv` and contains the following columns:

- `Timestamp`: The timestamp of the sample (ISO string)
- `Ch0 Act`: Activation level of sEMG Channel 0
- `Ch0 Env`: Envelope of sEMG Channel 0
- `Ch1 Act`: Activation level of sEMG Channel 1
- `Ch1 Env`: Envelope of sEMG Channel 1
- `Action`: The class label representing a specific physical action

---

## 🧠 Machine Learning Pipeline

### 1. Preprocessing
- **Feature Selection**: The model uses four input features: `Ch0 Act`, `Ch0 Env`, `Ch1 Act`, `Ch1 Env`.
- **Scaling**: Features are normalized using `StandardScaler` for zero-mean and unit-variance scaling.
- **Label Encoding**: Action labels are encoded into integers using `LabelEncoder`.

### 2. Sequence Generation
The time-series data is transformed into sequences using a sliding window approach:

```python
def create_sequences(X, y, seq_length=50):
    Xs, ys = [], []
    for i in range(len(X) - seq_length):
        Xs.append(X[i:i+seq_length])
        ys.append(y[i+seq_length])
    return np.array(Xs), np.array(ys)
```

This provides temporal context to the model by allowing it to learn from a window of 50 past frames.

### 3. Model Architecture

A 1D CNN is used to capture temporal patterns in the multivariate sEMG data. The architecture is:

- `Conv1D(64, kernel_size=3, activation='relu')`
- `MaxPooling1D(pool_size=2)`
- `Conv1D(128, kernel_size=3, activation='relu')`
- `GlobalAveragePooling1D()`
- `Dense(64, activation='relu')`
- `Dense(output_classes, activation='softmax')`

Loss: Sparse categorical cross-entropy  
Optimizer: Adam

The model is trained for 30 epochs with validation split.

---

## 💾 Saving Model Artifacts

After training:
- Model is saved as `semg_model.h5`
- Feature scaler is saved as `scaler.pkl`
- Label encoder is saved as `label_encoder.pkl`

---

## 🔌 Real-Time Inference (WebSocket)

A FastAPI server listens for real-time data streamed from a WebSocket (`localhost:3000/ws`). Incoming JSON messages are expected in the following format:

```json
{
  "ch0": { "a": float, "e": float },
  "ch1": { "a": float, "e": float }
}
```

These are appended to a buffer (`deque` of size 50). Once the buffer is full, the model performs inference on the sliding window and returns a classification label.

### Server Launch

```bash
uvicorn semg_websocket_server:app --reload --host 0.0.0.0 --port 8000
```

### Output

The server returns predicted class labels through the `/ws` WebSocket endpoint.

---

## 📦 Deployment Stack

- **Language**: Python 3.8+
- **Libraries**:
  - TensorFlow (for model training and inference)
  - FastAPI (for WebSocket server)
  - websockets (for internal proxy to data source)
  - scikit-learn (for preprocessing)

---

## 🧪 Testing

You can simulate real-time data by emitting JSON packets with the appropriate structure using Node.js or another WebSocket client.

---

## 📄 For Thesis Reference

This project demonstrates:
- Time-series classification using deep learning
- Preprocessing and modeling of biosignals
- Real-time streaming classification architecture
- Integration of machine learning with WebSocket I/O
- End-to-end deployment from CSV to inference

---
