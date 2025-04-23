

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class BaseModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def pad_data(self, data):
        max_length = max(len(features) for features, _ in data)
        padded_data = [(np.pad(features, (0, max_length - len(features)), mode='constant'), label) for features, label in data]
        return padded_data


class AmplitudeModel(BaseModel):
    def load_data(self, folder_path, label):
        data = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path)
                amplitudes = df['Amplitudes'].apply(lambda x: np.fromstring(x.strip("[]"), sep=', ')).tolist()
                data.extend([(amp, label) for amp in amplitudes])
        
        return self.pad_data(data)


class AmplitudePhaseModel(BaseModel):
    def load_data(self, folder_path, label):
        data = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path)
                amplitudes = df['Amplitudes'].apply(lambda x: np.fromstring(x.strip("[]"), sep=', ')).tolist()
                phases = df['Phases'].apply(lambda x: np.fromstring(x.strip("[]"), sep=', ')).tolist()
                
                combined_features = [np.concatenate((amp, phase)) for amp, phase in zip(amplitudes, phases)]
                data.extend([(features, label) for features in combined_features])
        
        return self.pad_data(data)


class FullCSIFeatureModel(BaseModel):
    def load_data(self, folder_path, label):
        data = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path)
                amplitudes = df['Amplitudes'].apply(lambda x: np.fromstring(x.strip("[]"), sep=', ')).tolist()
                phases = df['Phases'].apply(lambda x: np.fromstring(x.strip("[]"), sep=', ')).tolist()
                additional_features = df[['RSSI', 'Rate', 'Noise_Floor', 'Channel', 'Signal_Length']].values
                
                combined_features = [np.concatenate((amp, phase, extra)) for amp, phase, extra in zip(amplitudes, phases, additional_features)]
                data.extend([(features, label) for features in combined_features])
        
        return self.pad_data(data)






