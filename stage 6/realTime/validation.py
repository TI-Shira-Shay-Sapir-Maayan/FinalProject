# validation.py

import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# טוען מודל ואת הדאטה לפי שם

def load_model_and_data(model_name):
    model = joblib.load(f"saved_model_{model_name}.pkl")
    X_test, y_test = joblib.load(f"test_data_{model_name}.pkl")
    return model, X_test, y_test

# בודק מודל בודד לפי שם

def validate_model(model, X_test, y_test, model_name, axes):
    y_pred = model.predict(X_test)
    print(f"\n✅ Classification Report ({model_name}):")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes)
    axes.set_title(f"{model_name} Confusion Matrix")
    axes.set_xlabel("Predicted")
    axes.set_ylabel("True")
    axes.set_xticklabels(['No Movement', 'Movement'])
    axes.set_yticklabels(['No Movement', 'Movement'], rotation=0)

if __name__ == "__main__":
    model_names = ["amplitude", "amplitude_phase", "full_csi"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for i, name in enumerate(model_names):
        model, X_test, y_test = load_model_and_data(name)
        validate_model(model, X_test, y_test, name, axes[i])

    plt.tight_layout()
    plt.savefig("all_models_results.png")
    plt.show()

    print("\n🎉 the models saved as an : all_models_results.png")