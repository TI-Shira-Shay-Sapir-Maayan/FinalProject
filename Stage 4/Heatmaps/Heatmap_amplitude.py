import serial
import matplotlib.pyplot as plt
import numpy as np
import re

# הגדרת פורט והגדרות תקשורת
PORT = "COM10"  # עדכון הפורט
BAUD_RATE = 115200
TIMEOUT = 5

# דפוס רגולרי לחילוץ אמפליטודה ו-Phase מתוך המידע
PATTERN = re.compile(r"Subcarrier (\d+): Amplitude = ([\d.]+), Phase = [-\d.]+")
NUM_SUBCARRIERS = 64  # מספר ה-subcarriers

def read_and_plot_heatmap(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    
    # מטריצה שתשמור על 30 שורות עבור חלון הזזה, 64 עמודות (לכל subcarrier)
    window_size = 30
    data_matrix = np.zeros((window_size, NUM_SUBCARRIERS))  # שורות = זמן, עמודות = subcarriers
    max_amplitude = 1  # אתחול של מקסימום האמפליטודה (בהתחלה 1 כדי למנוע חישוב עם 0)
    
    # יצירת הגרף
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 8))  # גרף בגודל 12x8 אינצ'ים
    heatmap = None  # משתנה לאחסון טבלת החום
    
    subcarrier_data = np.zeros(NUM_SUBCARRIERS)  # רשימה שתאכסן את הנתונים עבור כל subcarrier
    num_received = 0  # סופר את מספר ה-subcarriers שהתקבלו בעבור האיטרציה הנוכחית
    
    try:
        while True:
            line_data = ser.readline().decode("utf-8").strip()  # קריאת שורה מתוך הפורט
            match = PATTERN.search(line_data)  # חיפוש הנתונים לפי הפטרן
            
            if match:
                try:
                    subcarrier = int(match.group(1))  # חילוץ ה-subcarrier
                    amplitude = float(match.group(2))  # חילוץ האמפליטודה
                    
                    # נרמול הערך של האמפליטודה
                    if amplitude > max_amplitude:
                        max_amplitude = amplitude  # עדכון המקסימום אם נמצא ערך גבוה יותר
                    normalized_amplitude = amplitude / max_amplitude  # נרמול
                    
                    # שמירת הערך של ה-subcarrier במערך
                    subcarrier_data[subcarrier] = normalized_amplitude
                    num_received += 1  # הגדלת הסופר
                    
                    # אם התקבלו כל 64 ה-subcarriers
                    if num_received == NUM_SUBCARRIERS:
                        # הזזת כל הנתונים שורה אחת למעלה
                        data_matrix[1:, :] = data_matrix[:-1, :]  # הזזת שורות למעלה, בלי שינוי בנתונים
                        
                        # הוספת השורה החדשה (הנתונים החדשים)
                        data_matrix[0, :] = subcarrier_data  # הוספת נתוני ה-subcarrier בשורה החדשה
                        
                        # יצירת או עדכון המפה החמה
                        if heatmap is None:
                            heatmap = ax.imshow(data_matrix, aspect='auto', cmap='viridis', interpolation='nearest')
                            plt.colorbar(heatmap, label='Normalized Amplitude')  # הוספת סרגל צבעים
                        else:
                            heatmap.set_data(data_matrix)  # עדכון המפה
                            heatmap.set_clim(vmin=0, vmax=1)  # עדכון טווח הצבעים ל- [0, 1]
                        
                        # הצגת המפה
                        plt.draw()
                        plt.pause(0.1)  # תהליך בזמן אמת
                        
                        # אפס את הנתונים והסופר עבור האיטרציה הבאה
                        subcarrier_data = np.zeros(NUM_SUBCARRIERS)
                        num_received = 0
                        
                except ValueError as e:
                    print(f"Error processing subcarrier data: {e}")
            
            # הגדרת הצירים והסימונים
            ax.set_xlabel('Subcarrier')  # שם לציר ה-X
            ax.set_ylabel('Time (samples)')  # שם לציר ה-Y
            ax.set_xticks(range(0, 64, 4))  # הצגת subcarriers כל 4
            ax.set_xticklabels(range(0, 64, 4))
            
            # עדכון טווח ציר ה-Y כך ש-0 יהיה למטה ו-30 למעלה
            ax.set_ylim(0, window_size - 1)  # טווח הציר [0, window_size-1] כך ש-0 יהיה למטה
            
    except KeyboardInterrupt:
        print("Stopped reading.")
    finally:
        plt.ioff()  # סיום הצגת הגרף
        plt.show()

# קריאה לפונקציה
read_and_plot_heatmap(PORT, BAUD_RATE, TIMEOUT)
