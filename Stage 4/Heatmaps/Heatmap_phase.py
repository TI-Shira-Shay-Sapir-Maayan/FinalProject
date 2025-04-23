import serial
import matplotlib.pyplot as plt
import numpy as np
import re

# הגדרת פורט והגדרות תקשורת
PORT = "COM10"  # עדכון הפורט
BAUD_RATE = 115200
TIMEOUT = 5

# דפוס רגולרי לחילוץ פאזה מתוך המידע
PATTERN = re.compile(r"Subcarrier (\d+): Amplitude = ([\d.]+), Phase = ([\d.-]+)")
NUM_SUBCARRIERS = 64  # מספר ה-subcarriers

def read_and_plot_heatmap(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    
    # מטריצות לזיכרון של 30 דגימות זמן עבור כל 64 ה-subcarriers
    window_size = 30
    phase_matrix = np.zeros((window_size, NUM_SUBCARRIERS))  # שמירת הפאזה בכל זמן עבור כל ה-subcarriers
    
    # יצירת הגרפים
    plt.ion()
    fig, ax = plt.subplots(figsize=(14, 8))  # גרף בגודל 14x8 אינצ'ים
    
    phase_heatmap = None  # משתנה לאחסון המפה החמה של הפאזה
    
    subcarrier_data_phase = np.zeros(NUM_SUBCARRIERS)  # רשימה שתאכסן את הנתונים עבור כל subcarrier
    num_received = 0  # סופר את מספר ה-subcarriers שהתקבלו בעבור האיטרציה הנוכחית
    
    try:
        while True:
            line_data = ser.readline().decode("utf-8").strip()  # קריאת שורה מתוך הפורט
            match = PATTERN.search(line_data)  # חיפוש הנתונים לפי הפטרן
            
            if match:
                try:
                    subcarrier = int(match.group(1))  # חילוץ ה-subcarrier
                    amplitude = float(match.group(2))  # חילוץ האמפליטודה (לא בשימוש כאן)
                    phase = float(match.group(3))  # חילוץ הפאזה
                    
                    # נרמול של הפאזה
                    normalized_phase = np.unwrap([phase])[0]  # נרמול הפאזה בין -pi ל-pi
                    
                    # שמירת הפאזה במערך
                    subcarrier_data_phase[subcarrier] = normalized_phase
                    num_received += 1  # הגדלת הסופר
                    
                    # אם התקבלו כל 64 ה-subcarriers
                    if num_received == NUM_SUBCARRIERS:
                        # הזזת כל הנתונים שורה אחת למעלה
                        phase_matrix[1:, :] = phase_matrix[:-1, :]  # הזזת שורות למעלה, בלי שינוי בנתונים
                        
                        # הוספת השורה החדשה (הנתונים החדשים)
                        phase_matrix[0, :] = subcarrier_data_phase  # הוספת נתוני הפאזה בשורה החדשה
                        
                        # יצירת או עדכון המפה החמה
                        if phase_heatmap is None:
                            phase_heatmap = ax.imshow(phase_matrix, aspect='auto', cmap='coolwarm', interpolation='nearest')
                            plt.colorbar(phase_heatmap, label='Phase (radians)')  # הוספת סרגל צבעים
                        else:
                            phase_heatmap.set_data(phase_matrix)  # עדכון המפה
                            phase_heatmap.set_clim(vmin=-np.pi, vmax=np.pi)  # עדכון טווח הצבעים ל- [-pi, pi]
                        
                        # הצגת המפה
                        plt.draw()
                        plt.pause(0.1)  # תהליך בזמן אמת
                        
                        # אפס את הנתונים והסופר עבור האיטרציה הבאה
                        subcarrier_data_phase = np.zeros(NUM_SUBCARRIERS)
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
