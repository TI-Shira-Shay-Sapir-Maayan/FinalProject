import serial
import matplotlib
import matplotlib.pyplot as plt

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_he_siga2(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    he_siga2_data = []  # רשימה לאחסון נתוני ה-he_siga2
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="he_siga2", color="green", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 5000000)  # טווח ראשוני עבור ציר ה-Y (יש להתאים לטווח הצפוי של הנתון)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("he_siga2")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating he_siga2 graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "he_siga2:" בשורה, ננסה לחלץ את הערך
            if "he_siga2:" in line_data:
                try:
                    # חילוץ ה-he_siga2 מתוך השורה
                    he_siga2 = int(line_data.split("he_siga2:")[1].split(",")[0].strip())
                    print(f"Parsed he_siga2: {he_siga2}")  # הדפסה של ה-he_siga2 שפורק
                    
                    he_siga2_data.append(he_siga2)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(he_siga2_data) > 50:
                        he_siga2_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(he_siga2_data)))  # עדכון ציר ה-X
                    line.set_ydata(he_siga2_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(he_siga2_data) - 50000, max(he_siga2_data) + 50000)  # התאמה של טווח ה-Y
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing he_siga2: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_he_siga2(PORT, BAUD_RATE, TIMEOUT)
