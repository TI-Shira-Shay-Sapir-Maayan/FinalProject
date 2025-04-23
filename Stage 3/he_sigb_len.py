import serial
import matplotlib
import matplotlib.pyplot as plt

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_he_sigb_len(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    he_sigb_len_data = []  # רשימה לאחסון נתוני ה-he_sigb_len
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="he_sigb_len", color="red", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 50)  # טווח ראשוני עבור ציר ה-Y (הגדלנו את טווח ה-Y)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("he_sigb_len")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating he_sigb_len graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "he_sigb_len:" בשורה, ננסה לחלץ את הערך
            if "he_sigb_len:" in line_data:
                try:
                    # חילוץ ה-he_sigb_len מתוך השורה
                    he_sigb_len = int(line_data.split("he_sigb_len:")[1].split(",")[0].strip())
                    print(f"Parsed he_sigb_len: {he_sigb_len}")  # הדפסה של ה-he_sigb_len שפורק
                    
                    he_sigb_len_data.append(he_sigb_len)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(he_sigb_len_data) > 50:
                        he_sigb_len_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(he_sigb_len_data)))  # עדכון ציר ה-X
                    line.set_ydata(he_sigb_len_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(he_sigb_len_data) - 5, max(he_sigb_len_data) + 5)  # התאמה של טווח ה-Y
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing he_sigb_len: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_he_sigb_len(PORT, BAUD_RATE, TIMEOUT)
