import serial
import matplotlib
import matplotlib.pyplot as plt

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_he_siga1(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    he_siga1_data = []  # רשימה לאחסון נתוני ה-he_siga1
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="he_siga1", color="purple", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 3e9)  # טווח ראשוני עבור ציר ה-Y (מכוונן לערכים גבוהים)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("he_siga1")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating he_siga1 graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"Received line: {line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "he_siga1:" בשורה, ננסה לחלץ את הערך
            if "he_siga1:" in line_data:
                try:
                    # חילוץ ה-he_siga1 מתוך השורה
                    he_siga1 = int(line_data.split("he_siga1:")[1].split(",")[0].strip())
                    print(f"Parsed he_siga1: {he_siga1}")  # הדפסה של ה-he_siga1 שפורק
                    
                    he_siga1_data.append(he_siga1)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(he_siga1_data) > 50:
                        he_siga1_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(he_siga1_data)))  # עדכון ציר ה-X
                    line.set_ydata(he_siga1_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(he_siga1_data) - 1e8, max(he_siga1_data) + 1e8)
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing he_siga1: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_he_siga1(PORT, BAUD_RATE, TIMEOUT)
