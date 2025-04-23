# predict_serial_all_models.py

import serial
import time
import joblib
import numpy as np
import ast

model_names = ["amplitude", "amplitude_phase", "full_csi"]

# טוען את כל המודלים בזיכרון
models = {}
for name in model_names:
    print(f"[INFO] טוען מודל: {name}")
    models[name] = joblib.load(f"saved_model_{name}.pkl")

# הגדרת החיבור ל-Serial
print("[INFO] מחכה לנתון מ-Serial (COM3)...")
ser = serial.Serial('COM10', 115200, timeout=2)
time.sleep(2)

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        # חיפוש המערך בתוך השורה
        if '[' not in line or ']' not in line:
            print("[SKIP] שורה ללא מערך CSI תקין")
            continue

        try:
            # חילוץ המחרוזת של רשימת CSI
            csi_str = line[line.index('['):line.index(']')+1]
            csi_values = ast.literal_eval(csi_str)
        except Exception as e:
            print(f"[SKIP] לא הצלחתי לקרוא מערך מתוך השורה: {e}")
            continue

        if not isinstance(csi_values, list) or len(csi_values) != 128:
            print(f"[SKIP] מערך באורך לא תקין ({len(csi_values)}), דילוג")
            continue

        # חילוץ תכונות (כמו שנעשה בקובץ CSV): מחלק ל־2 - amplitude + phase
        amplitudes = csi_values[:64]
        phases = csi_values[64:]
        features = np.array(amplitudes + phases).reshape(1, -1)

        print("\n📡 דגימה חדשה התקבלה - תוצאות:")
        for name, model in models.items():
            pred = model.predict(features)[0]
            label = "Movement" if pred == 1 else "No Movement"
            print(f"[{name.upper()}] → {label}")
        break  # לאחר דגימה אחת

except KeyboardInterrupt:
    print("[EXIT] משתמש")
except Exception as e:
    print(f"[ERROR] שגיאה: {e}")