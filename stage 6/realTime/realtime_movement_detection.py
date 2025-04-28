import serial
import time
import joblib
import numpy as np
import ast
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_names = ["amplitude", "amplitude_phase", "full_csi"]
models = {}
counters = {}

# Load all models
for name in model_names:
    model_path = os.path.join(BASE_DIR, f"saved_model_{name}.pkl")
    if not os.path.exists(model_path):
        print(f"[WARNING] File {model_path} not found, skipping...")
        continue
    print(f"[INFO] Loading model: {name}")
    models[name] = joblib.load(model_path)
    counters[name] = {"movement": 0, "no_movement": 0}

# Open Serial
print("[INFO] Waiting for data from Serial (COM10)...")
ser = serial.Serial('COM10', 115200, timeout=2)
time.sleep(2)

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        if '[' not in line or ']' not in line:
            print("[SKIP] Line without CSI array")
            continue

        try:
            # חלוקת השורה לקידומת ומערך
            prefix_part = line.split('[')[0].strip(',')
            array_part = line[line.index('['):line.index(']')+1]

            prefix_values = [x.strip() for x in prefix_part.split(',') if x.strip()]
            csi_values = ast.literal_eval(array_part)

        except Exception as e:
            print(f"[SKIP] Failed to parse line: {e}")
            continue

        if not isinstance(csi_values, list) or len(csi_values) != 128:
            print(f"[SKIP] Invalid CSI array length ({len(csi_values)}), skipping...")
            continue

        # חילוץ 5 הפיצ'רים מתוך ה־prefix
        try:
            RSSI = float(prefix_values[2])
            Rate = float(prefix_values[3])
            Noise_Floor = float(prefix_values[11])
            Channel = float(prefix_values[7])
            Signal_Length = float(prefix_values[4])
        except Exception as e:
            print(f"[SKIP] Failed to extract additional features: {e}")
            continue

        amplitudes = csi_values[:64]
        phases = csi_values[64:]
        extra_features = [RSSI, Rate, Noise_Floor, Channel, Signal_Length]

        # לבנות את הפיצ'ר המלא
        full_features = np.concatenate((amplitudes, phases, extra_features)).reshape(1, -1)

        print("\n📡 New sample received - Predictions:")

        for name, model in models.items():
            expected_features = model.n_features_in_

            if expected_features == 64:
                features = np.array(amplitudes).reshape(1, -1)
            elif expected_features == 128:
                features = np.array(csi_values).reshape(1, -1)
            elif expected_features == 133:
                features = full_features
            else:
                print(f"[SKIP] Model {name} expects {expected_features} features - skipping...")
                continue

            pred = model.predict(features)[0]
            label = "Movement" if pred == 1 else "No Movement"
            print(f"[{name.upper()}] → {label}")

            if pred == 1:
                counters[name]["movement"] += 1
            else:
                counters[name]["no_movement"] += 1


except KeyboardInterrupt:
    print("[EXIT] Interrupted by user - Calculating statistics...")

    print("\n📊 Summary of Predictions:")

    for name in model_names:
        if name not in counters:
            continue
        total = counters[name]["movement"] + counters[name]["no_movement"]
        if total == 0:
            continue
        percent_movement = counters[name]["movement"] / total * 100
        percent_no_movement = counters[name]["no_movement"] / total * 100

        print(f"\nModel: {name.upper()}")
        print(f"Total Samples: {total}")
        print(f"Movement Predictions: {percent_movement:.2f}%")
        print(f"No Movement Predictions: {percent_no_movement:.2f}%")

except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
