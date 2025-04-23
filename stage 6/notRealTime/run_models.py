from models import AmplitudeModel, AmplitudePhaseModel, FullCSIFeatureModel
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import serial
import time

# טוען את כל הנתונים לאימון המודל

def load_all_data(model_class):
    model = model_class()
    data_with_moves = model.load_data('dataset_withmoves', 1)
    data_no_moves = model.load_data('dataset', 0)

    all_data = data_with_moves + data_no_moves
    X = np.array([item[0] for item in all_data])
    y = np.array([item[1] for item in all_data])

    return X, y

# אימון מודל והצגת מטריצת בלבול

def run_model(model_class, model_name, axes):
    X, y = load_all_data(model_class)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = model_class()
    model.model.fit(X_train, y_train)
    y_pred = model.model.predict(X_test)

    print(f"Classification Report ({model_name}):")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes)
    axes.set_title(f'{model_name} Confusion Matrix')
    axes.set_xlabel('Predicted Labels')
    axes.set_ylabel('True Labels')
    axes.set_xticklabels(['No Movement', 'Movement'])
    axes.set_yticklabels(['No Movement', 'Movement'])

    return model.model  # מחזיר את המודל המאומן

# קריאה מה-Serial לצורך חיזוי על נתונים חיים

def listen_to_serial(model):
    print("[INFO] מאזין לנתונים חיים מ-Serial (COM3)...")
    ser = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)  # זמן חיבור

    while True:
        try:
            line = ser.readline().decode().strip()
            if not line:
                continue

            raw_values = [float(x) for x in line.split(',') if x.strip()]
            if len(raw_values) != 64:
                print("[WARNING] קלט לא תקין - דילוג")
                continue

            # חיזוי
            x = np.array(raw_values).reshape(1, -1)
            prediction = model.predict(x)[0]
            print("[LIVE PREDICT] Movement Detected" if prediction == 1 else "[LIVE PREDICT] No Movement")

        except KeyboardInterrupt:
            print("[EXIT] הופסק על ידי המשתמש")
            break
        except Exception as e:
            print(f"[ERROR] שגיאה: {e}")

if __name__ == "__main__":
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))

    # מאמן שלושה מודלים ומציג מטריצות בלבול
    print("[INFO] מתחיל אימון שלושת המודלים...")
    model1 = run_model(AmplitudeModel, "Amplitude Model", axes[0])
    model2 = run_model(AmplitudePhaseModel, "Amplitude + Phase Model", axes[1])
    model3 = run_model(FullCSIFeatureModel, "Full CSI Feature Model", axes[2])

    plt.tight_layout()
    plt.savefig("output_plot.png")
    print("[INFO] נשמר גרף התוצאות כ-output_plot.png")

    # מפעיל מיידית מצב חיזוי חי בלי לשאול
    listen_to_serial(model1)