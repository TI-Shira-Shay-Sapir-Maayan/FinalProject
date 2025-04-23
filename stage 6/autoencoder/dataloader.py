import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataLoader:
    def __init__(self, data_folder, num_subcarriers=64):
        self.data_folder = data_folder
        self.num_subcarriers = num_subcarriers
        self.data = None

    def load_data(self):
        csv_files = [f for f in os.listdir(self.data_folder) if f.endswith('.csv')]
        data_frames = [pd.read_csv(os.path.join(self.data_folder, file)) for file in csv_files]
        self.data = pd.concat(data_frames, ignore_index=True)
        print(f"Loaded {len(csv_files)} files with {len(self.data)} rows.")

    # הפונקציה החסרה שהייתה הבעיה:
    def load_single_file(self, file_path):
        self.data = pd.read_csv(file_path)
        print(f"Loaded file {file_path} with {len(self.data)} rows.")

    def preprocess_data(self):
        def safe_eval(x):
            try:
                arr = eval(x)
                if isinstance(arr, list) and len(arr) == self.num_subcarriers:
                    return np.array(arr)
                else:
                    return np.zeros(self.num_subcarriers)
            except:
                return np.zeros(self.num_subcarriers)

        amplitudes = self.data['Amplitudes'].apply(safe_eval)
        amplitudes = np.vstack(amplitudes)
        
        scaler = StandardScaler()
        amplitudes_normalized = scaler.fit_transform(amplitudes)

        return amplitudes_normalized

    def split_data(self, data):
        X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)
        return X_train, X_test

