# train_model.py

from models import AmplitudeModel, AmplitudePhaseModel, FullCSIFeatureModel
from sklearn.model_selection import train_test_split
import numpy as np
import joblib
import os

# טוען את כל הנתונים

def load_all_data(model_class):
    model = model_class()
    data_with_moves = model.load_data('dataset_withmoves', 1)
    data_no_moves = model.load_data('dataset', 0)
    all_data = data_with_moves + data_no_moves
    X = np.array([item[0] for item in all_data])
    y = np.array([item[1] for item in all_data])
    return X, y

# מאמן ושומר כל מודל

def train_and_save(model_class, name):
    print(f"\n🔄 מאמן מודל: {name}")
    X, y = load_all_data(model_class)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_instance = model_class()
    model_instance.model.fit(X_train, y_train)

    model_filename = f"saved_model_{name}.pkl"
    test_data_filename = f"test_data_{name}.pkl"
    joblib.dump(model_instance.model, model_filename)
    joblib.dump((X_test, y_test), test_data_filename)

    print(f"✅ נשמרו: {model_filename}, {test_data_filename}")

if __name__ == "__main__":
    train_and_save(AmplitudeModel, "amplitude")
    train_and_save(AmplitudePhaseModel, "amplitude_phase")
    train_and_save(FullCSIFeatureModel, "full_csi")

    print("\n🎉 סיום אימון ושמירה של שלושת המודלים!")