import numpy as np
import matplotlib.pyplot as plt
import csv

# קריאת הנתונים מהקובץ
file_path = "csi_runs_output.csv"  # ודאי שהקובץ באותה תיקייה
subcarrier_indices = []
amplitudes = []
phases = []

with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # דילוג על הכותרת הראשונה
    next(reader)  # דילוג על הכותרת השנייה

    for row in reader:
        if len(row) < 3:
            continue
        try:
            subcarrier_indices.append(int(row[0]))  # Subcarrier
            amplitudes.append(float(row[1]))  # Amplitude
            phases.append(float(row[2]))  # Phase
        except ValueError:
            continue

# יצירת תדרים חיוביים ושליליים עבור FFT של 64 תתי-נשאים
N = 64
subcarriers = np.fft.fftshift(np.fft.fftfreq(N))

# יצירת גרף המשרעת
plt.figure(figsize=(10, 6))
plt.stem(subcarriers, amplitudes[:N])
plt.title("Subcarriers in OFDM: Positive and Negative Frequencies (Amplitude)")
plt.xlabel("Subcarrier Index")
plt.ylabel("Amplitude")
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')

# יצירת גרף הפאזה
plt.figure(figsize=(10, 6))
plt.stem(subcarriers, phases[:N])
plt.title("Subcarriers in OFDM: Positive and Negative Frequencies (Phase)")
plt.xlabel("Subcarrier Index")
plt.ylabel("Phase")
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')

# הצגת הגרפים
plt.show()