import serial
import matplotlib.pyplot as plt
import numpy as np
import re

# הגדרת פורט והגדרות תקשורת
PORT = "COM10"  # עדכון הפורט
BAUD_RATE = 115200
TIMEOUT = 5

# דפוס רגולרי לחילוץ אמפליטודה ופאזה מתוך המידע
PATTERN = re.compile(r"Subcarrier (\d+): Amplitude = ([\d.]+), Phase = ([\d.-]+)")
NUM_SUBCARRIERS = 64  # מספר ה-subcarriers

def read_and_plot_heatmap(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    
    # מטריצה שתשמור על 30 שורות עבור חלון הזזה, 64 עמודות (לכל subcarrier)
    window_size = 30
    amplitude_matrix = np.zeros((window_size, NUM_SUBCARRIERS))  # שורות = זמן, עמודות = subcarriers עבור האמפליטודה
    phase_matrix = np.zeros((window_size, NUM_SUBCARRIERS))  # שורות = זמן, עמודות = subcarriers עבור הפאזה
    
    max_amplitude = 1  # אתחול של מקסימום האמפליטודה (בהתחלה 1 כדי למנוע חישוב עם 0)
    
    # יצירת הגרפים
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))  # שני גרפים באורך 12x8 אינצ'ים
    
    amplitude_heatmap = None  # משתנה לאחסון טבלת החום של האמפליטודה
    phase_heatmap = None  # משתנה לאחסון טבלת החום של הפאזה
    
    subcarrier_data_amplitude = np.zeros(NUM_SUBCARRIERS)  # רשימה שתאכסן את נתוני האמפליטודה עבור כל subcarrier
    subcarrier_data_phase = np.zeros(NUM_SUBCARRIERS)  # רשימה שתאכסן את נתוני הפאזה עבור כל subcarrier
    num_received = 0  # סופר את מספר ה-subcarriers שהתקבלו בעבור האיטרציה הנוכחית
    
    try:
        while True:
            line_data = ser.readline().decode("utf-8").strip()  # קריאת שורה מתוך הפורט
            match = PATTERN.search(line_data)  # חיפוש הנתונים לפי הפטרן
            
            if match:
                try:
                    subcarrier = int(match.group(1))  # חילוץ ה-subcarrier
                    amplitude = float(match.group(2))  # חילוץ האמפליטודה
                    phase = float(match.group(3))  # חילוץ הפאזה
                    
                    # נרמול האמפליטודה
                    if amplitude > max_amplitude:
                        max_amplitude = amplitude  # עדכון המקסימום אם נמצא ערך גבוה יותר
                    normalized_amplitude = amplitude / max_amplitude  # נרמול
                    
                    # נרמול של הפאזה לטווח [0, 1]
                    normalized_phase = (phase + np.pi) / (2 * np.pi)  # נרמול ל-[0, 1]
                    
                    # שמירת הערכים במערכים המתאימים
                    subcarrier_data_amplitude[subcarrier] = normalized_amplitude
                    subcarrier_data_phase[subcarrier] = normalized_phase
                    num_received += 1  # הגדלת הסופר
                    
                    # אם התקבלו כל 64 ה-subcarriers
                    if num_received == NUM_SUBCARRIERS:
                        # הזזת כל הנתונים שורה אחת למעלה
                        amplitude_matrix[1:, :] = amplitude_matrix[:-1, :]
                        phase_matrix[1:, :] = phase_matrix[:-1, :]
                        
                        # הוספת השורה החדשה (הנתונים החדשים)
                        amplitude_matrix[0, :] = subcarrier_data_amplitude
                        phase_matrix[0, :] = subcarrier_data_phase
                        
                        # יצירת או עדכון המפות החמות
                        if amplitude_heatmap is None:
                            amplitude_heatmap = ax1.imshow(amplitude_matrix, aspect='auto', cmap='viridis', interpolation='nearest')
                            plt.colorbar(amplitude_heatmap, ax=ax1, label='Normalized Amplitude')
                        else:
                            amplitude_heatmap.set_data(amplitude_matrix)
                            amplitude_heatmap.set_clim(vmin=0, vmax=1)
                        
                        if phase_heatmap is None:
                            phase_heatmap = ax2.imshow(phase_matrix, aspect='auto', cmap='coolwarm', interpolation='nearest')
                            plt.colorbar(phase_heatmap, ax=ax2, label='Normalized Phase')
                        else:
                            phase_heatmap.set_data(phase_matrix)
                            phase_heatmap.set_clim(vmin=0, vmax=1)
                        
                        # הצגת המפות
                        plt.draw()
                        plt.pause(0.1)  # תהליך בזמן אמת
                        
                        # אפס את הנתונים והסופר עבור האיטרציה הבאה
                        subcarrier_data_amplitude = np.zeros(NUM_SUBCARRIERS)
                        subcarrier_data_phase = np.zeros(NUM_SUBCARRIERS)
                        num_received = 0
                        
                except ValueError as e:
                    print(f"Error processing subcarrier data: {e}")
            
            # הגדרת הצירים והסימונים
            ax1.set_xlabel('Subcarrier')
            ax1.set_ylabel('Time (samples)')
            ax1.set_xticks(range(0, 64, 4))
            ax1.set_xticklabels(range(0, 64, 4))
            ax1.set_ylim(0, window_size - 1)
            
            ax2.set_xlabel('Subcarrier')
            ax2.set_ylabel('Time (samples)')
            ax2.set_xticks(range(0, 64, 4))
            ax2.set_xticklabels(range(0, 64, 4))
            ax2.set_ylim(0, window_size - 1)
            
    except KeyboardInterrupt:
        print("Stopped reading.")
    finally:
        plt.ioff()  # סיום הצגת הגרף
        plt.show()

# קריאה לפונקציה
read_and_plot_heatmap(PORT, BAUD_RATE, TIMEOUT)
