import serial
import time
import joblib
import numpy as np
import ast
import os
import pandas as pd
from sklearn.metrics import confusion_matrix

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_names = ["amplitude", "amplitude_phase", "full_csi"]
models = {}
counters = {}
predictions = {}

# Load models
for name in model_names:
    model_path = os.path.join(BASE_DIR, f"saved_model_{name}.pkl")
    if not os.path.exists(model_path):
        print(f"[WARNING] File {model_path} not found.")
        continue
    print(f"[INFO] Loading model: {name}")
    models[name] = joblib.load(model_path)
    counters[name] = {"movement": 0, "no_movement": 0}
    predictions[name] = {"y_true": [], "y_pred": []}

# Open serial port
print("[INFO] Waiting for data from COM10...")
ser = serial.Serial('COM10', 115200, timeout=2)
time.sleep(10)
print("[INFO] Starting to read data...")

sample_count = 0

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line or '[' not in line or ']' not in line:
            continue

        try:
            prefix_part = line.split('[')[0].strip(',')
            array_part = line[line.index('['):line.index(']')+1]
            prefix_values = [x.strip() for x in prefix_part.split(',') if x.strip()]
            csi_values = ast.literal_eval(array_part)
        except Exception:
            continue

        if not isinstance(csi_values, list) or len(csi_values) != 128:
            continue

        try:
            RSSI = float(prefix_values[2])
            Rate = float(prefix_values[3])
            Noise_Floor = float(prefix_values[11])
            Channel = float(prefix_values[7])
            Signal_Length = float(prefix_values[4])
        except Exception:
            continue

        amplitudes = csi_values[:64]
        phases = csi_values[64:]
        extra_features = [RSSI, Rate, Noise_Floor, Channel, Signal_Length]
        full_features = np.concatenate((amplitudes, phases, extra_features)).reshape(1, -1)

        print("\n📡 New sample - Predictions:")
        for name, model in models.items():
            expected = model.n_features_in_
            if expected == 64:
                features = np.array(amplitudes).reshape(1, -1)
            elif expected == 128:
                features = np.array(csi_values).reshape(1, -1)
            elif expected == 133:
                features = full_features
            else:
                continue

            pred = model.predict(features)[0]
            label = "Movement" if pred == 1 else "No Movement"
            print(f"[{name.upper()}] → {label}")

            if pred == 1:
                counters[name]["movement"] += 1
            else:
                counters[name]["no_movement"] += 1

            # Simulate true label as 1 (movement) for now
            predictions[name]["y_true"].append(1)  # <-- לשלב הבא: שים כאן אמת אמיתית אם קיימת
            predictions[name]["y_pred"].append(pred)

        sample_count += 1

        if sample_count % 100 == 0:
            print(f"\n📊 Confusion matrices after {sample_count} samples:")
            for name in model_names:
                if name not in predictions:
                    continue
                y_true = predictions[name]["y_true"]
                y_pred = predictions[name]["y_pred"]
                if len(y_true) >= 2:
                    print(f"\nModel: {name.upper()}")
                    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
                    cm_df = pd.DataFrame(
                        cm,
                        index=["Actual No Movement", "Actual Movement"],
                        columns=["Predicted No Movement", "Predicted Movement"]
                    )
                    print(cm_df)

except KeyboardInterrupt:
    print("\n[EXIT] Interrupted - Final Summary:\n")
    for name in model_names:
        if name not in counters:
            continue
        m = counters[name]["movement"]
        n = counters[name]["no_movement"]
        total = m + n
        if total == 0:
            continue
        print(f"\nModel: {name.upper()}")
        print(f"Total Predictions: {total}")
        print(f"Movement: {m} ({m/total:.2%})")
        print(f"No Movement: {n} ({n/total:.2%})")
        print("Confusion Matrix:")
        cm = confusion_matrix(predictions[name]["y_true"], predictions[name]["y_pred"], labels=[0, 1])
        cm_df = pd.DataFrame(
            cm,
            index=["Actual No Movement", "Actual Movement"],
            columns=["Predicted No Movement", "Predicted Movement"]
        )
        print(cm_df)

except Exception as e:
    print(f"[ERROR] {e}")
        
